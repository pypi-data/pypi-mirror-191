# Copyright 2018 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""The GaussianProcess distribution class."""

import functools
import warnings

# Dependency imports
import numpy as np
from tensorflow_probability.python.internal.backend.numpy.compat import v2 as tf

from tensorflow_probability.substrates.numpy.bijectors import identity as identity_bijector
from tensorflow_probability.substrates.numpy.bijectors import softplus as softplus_bijector
from tensorflow_probability.substrates.numpy.distributions import cholesky_util
from tensorflow_probability.substrates.numpy.distributions import distribution
from tensorflow_probability.substrates.numpy.distributions import kullback_leibler
from tensorflow_probability.substrates.numpy.distributions import mvn_linear_operator
from tensorflow_probability.substrates.numpy.distributions import normal
from tensorflow_probability.substrates.numpy.internal import auto_composite_tensor
from tensorflow_probability.substrates.numpy.internal import batch_shape_lib
from tensorflow_probability.substrates.numpy.internal import distribution_util
from tensorflow_probability.substrates.numpy.internal import dtype_util
from tensorflow_probability.substrates.numpy.internal import nest_util
from tensorflow_probability.substrates.numpy.internal import parameter_properties
from tensorflow_probability.substrates.numpy.internal import prefer_static as ps
from tensorflow_probability.python.internal import reparameterization
from tensorflow_probability.substrates.numpy.internal import tensor_util
from tensorflow_probability.substrates.numpy.internal import tensorshape_util
from tensorflow_probability.substrates.numpy.math import linalg
from tensorflow_probability.substrates.numpy.math.psd_kernels.internal import util as psd_kernels_util
from tensorflow_probability.python.internal.backend.numpy import deprecation  # pylint: disable=g-direct-tensorflow-import
from tensorflow_probability.python.internal.backend.numpy import nest  # pylint: disable=g-direct-tensorflow-import


__all__ = [
    'GaussianProcess',
    'make_cholesky_factored_marginal_fn'
]

JAX_MODE = False


def _add_diagonal_shift(matrix, shift):
  return tf.linalg.set_diag(
      matrix, tf.linalg.diag_part(matrix) + shift, name='add_diagonal_shift')


_ALWAYS_YIELD_MVN_DEPRECATION_WARNING = (
    '`always_yield_multivariate_normal` is deprecated. After 2023-02-15, this '
    'arg will be ignored, and behavior will be as though '
    '`always_yield_multivariate_normal=True`. This means that a'
    '`GaussianProcessRegressionModel` evaluated at a single index point will '
    'have event shape `[1]`. To reproduce the behavior of '
    '`always_yield_multivariate_normal=False` squeeze the rightmost singleton '
    'dimension from the output of `mean`, `sample`, etc.')


_GET_MARGINAL_DISTRIBUTION_ALREADY_WARNED = False


def make_cholesky_factored_marginal_fn(cholesky_fn):
  """Construct a `marginal_fn` for use with `tfd.GaussianProcess`.

  The returned function computes the Cholesky factorization of the input
  covariance plus a diagonal jitter, and uses that for the `scale` of a
  `tfd.MultivariateNormalLinearOperator`.

  Args:
    cholesky_fn: Callable which takes a single (batch) matrix argument and
        returns a Cholesky-like lower triangular factor.

  Returns:
    marginal_fn: A Python function that takes a location, covariance matrix,
      optional `validate_args`, `allow_nan_stats` and `name` arguments, and
      returns a `tfd.MultivariateNormalLinearOperator`.
  """
  def marginal_fn(
      loc,
      covariance,
      validate_args=False,
      allow_nan_stats=False,
      name='marginal_distribution'):
    scale = tf.linalg.LinearOperatorLowerTriangular(
        cholesky_fn(covariance),
        is_non_singular=True,
        name='GaussianProcessScaleLinearOperator')
    return mvn_linear_operator.MultivariateNormalLinearOperator(
        loc=loc,
        scale=scale,
        validate_args=validate_args,
        allow_nan_stats=allow_nan_stats,
        name=name)

  return marginal_fn


class GaussianProcess(
    distribution.Distribution, tf.__internal__.CompositeTensor):
  """Marginal distribution of a Gaussian process at finitely many points.

  A Gaussian process (GP) is an indexed collection of random variables, any
  finite collection of which are jointly Gaussian. While this definition applies
  to finite index sets, it is typically implicit that the index set is infinite;
  in applications, it is often some finite dimensional real or complex vector
  space. In such cases, the GP may be thought of as a distribution over
  (real- or complex-valued) functions defined over the index set.

  Just as Gaussian distributions are fully specified by their first and second
  moments, a Gaussian process can be completely specified by a mean and
  covariance function. Let `S` denote the index set and `K` the space in which
  each indexed random variable takes its values (again, often R or C). The mean
  function is then a map `m: S -> K`, and the covariance function, or kernel, is
  a positive-definite function `k: (S x S) -> K`. The properties of functions
  drawn from a GP are entirely dictated (up to translation) by the form of the
  kernel function.

  This `Distribution` represents the marginal joint distribution over function
  values at a given finite collection of points `[x[1], ..., x[N]]` from the
  index set `S`. By definition, this marginal distribution is just a
  multivariate normal distribution, whose mean is given by the vector
  `[ m(x[1]), ..., m(x[N]) ]` and whose covariance matrix is constructed from
  pairwise applications of the kernel function to the given inputs:

  ```none
      | k(x[1], x[1])    k(x[1], x[2])  ...  k(x[1], x[N]) |
      | k(x[2], x[1])    k(x[2], x[2])  ...  k(x[2], x[N]) |
      |      ...              ...                 ...      |
      | k(x[N], x[1])    k(x[N], x[2])  ...  k(x[N], x[N]) |
  ```

  For this to be a valid covariance matrix, it must be symmetric and positive
  definite; hence the requirement that `k` be a positive definite function
  (which, by definition, says that the above procedure will yield PD matrices).

  We also support the inclusion of zero-mean Gaussian noise in the model, via
  the `observation_noise_variance` parameter. This augments the generative model
  to

  ```none
  f ~ GP(m, k)
  (y[i] | f, x[i]) ~ Normal(f(x[i]), s)
  ```

  where

    * `m` is the mean function
    * `k` is the covariance kernel function
    * `f` is the function drawn from the GP
    * `x[i]` are the index points at which the function is observed
    * `y[i]` are the observed values at the index points
    * `s` is the scale of the observation noise.

  Note that this class represents an *unconditional* Gaussian process; it does
  not implement posterior inference conditional on observed function
  evaluations. This class is useful, for example, if one wishes to combine a GP
  prior with a non-conjugate likelihood using MCMC to sample from the posterior.

  #### Mathematical Details

  The probability density function (pdf) is a multivariate normal whose
  parameters are derived from the GP's properties:

  ```none
  pdf(x; index_points, mean_fn, kernel) = exp(-0.5 * y) / Z
  K = (kernel.matrix(index_points, index_points) +
       observation_noise_variance * eye(N))
  y = (x - mean_fn(index_points))^T @ K @ (x - mean_fn(index_points))
  Z = (2 * pi)**(.5 * N) |det(K)|**(.5)
  ```

  where:

  * `index_points` are points in the index set over which the GP is defined,
  * `mean_fn` is a callable mapping the index set to the GP's mean values,
  * `kernel` is `PositiveSemidefiniteKernel`-like and represents the covariance
    function of the GP,
  * `observation_noise_variance` represents (optional) observation noise.
  * `eye(N)` is an N-by-N identity matrix.

  #### Examples

  ##### Draw joint samples from a GP prior

  ```python
  import numpy as np
  from tensorflow_probability.python.internal.backend.numpy.compat import v2 as tf
  import tensorflow_probability as tfp; tfp = tfp.substrates.numpy

  tfd = tfp.distributions
  psd_kernels = tfp.math.psd_kernels

  num_points = 100
  # Index points should be a collection (100, here) of feature vectors. In this
  # example, we're using 1-d vectors, so we just need to reshape the output from
  # np.linspace, to give a shape of (100, 1).
  index_points = np.expand_dims(np.linspace(-1., 1., num_points), -1)

  # Define a kernel with default parameters.
  kernel = psd_kernels.ExponentiatedQuadratic()

  gp = tfd.GaussianProcess(kernel, index_points)

  samples = gp.sample(10)
  # ==> 10 independently drawn, joint samples at `index_points`

  noisy_gp = tfd.GaussianProcess(
      kernel=kernel,
      index_points=index_points,
      observation_noise_variance=.05)
  noisy_samples = noisy_gp.sample(10)
  # ==> 10 independently drawn, noisy joint samples at `index_points`
  ```

  ##### Optimize kernel parameters via maximum marginal likelihood.

  ```python
  # Suppose we have some data from a known function. Note the index points in
  # general have shape `[b1, ..., bB, f1, ..., fF]` (here we assume `F == 1`),
  # so we need to explicitly consume the feature dimensions (just the last one
  # here).
  f = lambda x: np.sin(10*x[..., 0]) * np.exp(-x[..., 0]**2)
  observed_index_points = np.expand_dims(np.random.uniform(-1., 1., 50), -1)
  # Squeeze to take the shape from [50, 1] to [50].
  observed_values = f(observed_index_points)

  # Define a kernel with trainable parameters.
  kernel = psd_kernels.ExponentiatedQuadratic(
      amplitude=tf.Variable(1., dtype=np.float64, name='amplitude'),
      length_scale=tf.Variable(1., dtype=np.float64, name='length_scale'))

  gp = tfd.GaussianProcess(kernel, observed_index_points)

  optimizer = tf.optimizers.Adam()

  @tf.function
  def optimize():
    with tf.GradientTape() as tape:
      loss = -gp.log_prob(observed_values)
    grads = tape.gradient(loss, gp.trainable_variables)
    optimizer.apply_gradients(zip(grads, gp.trainable_variables))
    return loss

  for i in range(1000):
    neg_log_likelihood = optimize()
    if i % 100 == 0:
      print("Step {}: NLL = {}".format(i, neg_log_likelihood))
  print("Final NLL = {}".format(neg_log_likelihood))
  ```

  """
  # pylint:disable=invalid-name

  @deprecation.deprecated_args(
      '2021-05-10',
      '`jitter` is deprecated; please use `marginal_fn` directly.',
      'jitter')
  @deprecation.deprecated_arg_values(
      '2023-02-15',
      _ALWAYS_YIELD_MVN_DEPRECATION_WARNING,
      always_yield_multivariate_normal=False)
  def __init__(self,
               kernel,
               index_points=None,
               mean_fn=None,
               observation_noise_variance=0.,
               marginal_fn=None,
               cholesky_fn=None,
               jitter=1e-6,
               always_yield_multivariate_normal=False,
               validate_args=False,
               allow_nan_stats=False,
               parameters=None,
               name='GaussianProcess',
               _check_marginal_cholesky_fn=True):
    """Instantiate a GaussianProcess Distribution.

    Args:
      kernel: `PositiveSemidefiniteKernel`-like instance representing the
        GP's covariance function.
      index_points: (nested) `Tensor` representing finite (batch of) vector(s)
        of points in the index set over which the GP is defined. Shape (or
        shape of each nested component) has the form `[b1, ..., bB, e, f1,
        ..., fF]` where `F` is the number of feature dimensions and must
        equal `kernel.feature_ndims` (or its corresponding nested component)
        and `e` is the number (size) of index points in each batch.
        Ultimately this distribution corresponds to a `e`-dimensional
        multivariate normal. The batch shape must be broadcastable with
        `kernel.batch_shape` and any batch dims yielded by `mean_fn`.
      mean_fn: Python `callable` that acts on `index_points` to produce a (batch
        of) vector(s) of mean values at `index_points`. Takes a (nested)
        `Tensor` of shape `[b1, ..., bB, f1, ..., fF]` and returns a `Tensor`
        whose shape is broadcastable with `[b1, ..., bB]`. Default value:
        `None` implies constant zero function.
      observation_noise_variance: `float` `Tensor` representing (batch of)
        scalar variance(s) of the noise in the Normal likelihood
        distribution of the model. If batched, the batch shape must be
        broadcastable with the shapes of all other batched parameters
        (`kernel.batch_shape`, `index_points`, etc.).
        Default value: `0.`
      marginal_fn: A Python callable that takes a location, covariance matrix,
        optional `validate_args`, `allow_nan_stats` and `name` arguments, and
        returns a multivariate normal subclass of `tfd.Distribution`.
        At most one of `cholesky_fn` and `marginal_fn` should be set.
        Default value: `None`, in which case a Cholesky-factorizing function
        is created using `make_cholesky_factored_marginal_fn` and the
        `cholesky_fn` argument.
      cholesky_fn: Callable which takes a single (batch) matrix argument and
        returns a Cholesky-like lower triangular factor.  Default value: `None`,
        in which case `make_cholesky_with_jitter_fn` is used with the `jitter`
        parameter. At most one of `cholesky_fn` and `marginal_fn` should be set.
      jitter: `float` scalar `Tensor` added to the diagonal of the covariance
        matrix to ensure positive definiteness of the covariance matrix, when
        `marginal_fn` and `cholesky_fn` is None.
        This argument is ignored if `cholesky_fn` is set.
        Default value: `1e-6`.
      always_yield_multivariate_normal: Deprecated. If `False` (the default), we
        produce a scalar `Normal` distribution when the number of
        `index_points` is statically known to be `1`. If `True`, we avoid
        this behavior, ensuring that the event shape will retain the `1` from
        `index_points`.
      validate_args: Python `bool`, default `False`. When `True` distribution
        parameters are checked for validity despite possibly degrading runtime
        performance. When `False` invalid inputs may silently render incorrect
        outputs.
        Default value: `False`.
      allow_nan_stats: Python `bool`, default `True`. When `True`,
        statistics (e.g., mean, mode, variance) use the value "`NaN`" to
        indicate the result is undefined. When `False`, an exception is raised
        if one or more of the statistic's batch members are undefined.
        Default value: `False`.
      parameters: For subclasses, a dict of constructor arguments.
      name: Python `str` name prefixed to Ops created by this class.
        Default value: "GaussianProcess".
      _check_marginal_cholesky_fn: Internal parameter -- do not use.

    Raises:
      ValueError: if `mean_fn` is not `None` and is not callable.
    """
    parameters = dict(locals()) if parameters is None else parameters
    with tf.name_scope(name) as name:
      if tf.nest.is_nested(kernel.feature_ndims):
        input_dtype = dtype_util.common_dtype(
            [kernel, index_points],
            dtype_hint=nest_util.broadcast_structure(
                kernel.feature_ndims, tf.float32))
        dtype = dtype_util.common_dtype(
            [observation_noise_variance, jitter], tf.float32)
      else:
        # If the index points are not nested, we assume they are of the same
        # float dtype as the GP.
        dtype = dtype_util.common_dtype(
            {
                'index_points': index_points,
                'observation_noise_variance': observation_noise_variance,
                'jitter': jitter
            }, tf.float32)
        input_dtype = dtype

      if index_points is not None:
        index_points = nest_util.convert_to_nested_tensor(
            index_points, dtype=input_dtype, name='index_points',
            convert_ref=False, allow_packing=True)
      jitter = tensor_util.convert_nonref_to_tensor(
          jitter, dtype=dtype, name='jitter')
      observation_noise_variance = tensor_util.convert_nonref_to_tensor(
          observation_noise_variance,
          dtype=dtype,
          name='observation_noise_variance')

      self._kernel = kernel
      self._index_points = index_points
      # Default to a constant zero function, borrowing the dtype from
      # index_points to ensure consistency.
      if mean_fn is None:
        mean_fn = lambda x: tf.zeros([1], dtype=dtype)
      else:
        if not callable(mean_fn):
          raise ValueError('`mean_fn` must be a Python callable')
      self._mean_fn = mean_fn
      self._observation_noise_variance = observation_noise_variance
      self._jitter = jitter
      self._cholesky_fn = cholesky_fn

      if (_check_marginal_cholesky_fn and
          marginal_fn is not None and cholesky_fn is not None):
        raise ValueError(
            'At most one of `marginal_fn` and `cholesky_fn` should be set.')
      if marginal_fn is None:
        if cholesky_fn is None:
          self._cholesky_fn = cholesky_util.make_cholesky_with_jitter_fn(jitter)
        self._marginal_fn = make_cholesky_factored_marginal_fn(
            self._cholesky_fn)
      else:
        self._marginal_fn = marginal_fn

      self._always_yield_multivariate_normal = always_yield_multivariate_normal
      with tf.name_scope('init'):
        super(GaussianProcess, self).__init__(
            dtype=dtype,
            reparameterization_type=reparameterization.FULLY_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            parameters=parameters,
            name=name)
    # pylint:enable=invalid-name

  def _is_univariate_marginal(self, index_points):
    """True if the given index_points would yield a univariate marginal.

    Args:
      index_points: the set of index set locations at which to compute the
      marginal Gaussian distribution. If this set is of size 1, the marginal is
      univariate.

    Returns:
      is_univariate: Boolean indicating whether the marginal is univariate or
      multivariate. In the case of dynamic shape in the number of index points,
      defaults to "multivariate" since that's the best we can do.
    """
    if self._always_yield_multivariate_normal:
      return False

    num_index_points = tf.nest.map_structure(
        lambda x, nd: tf.compat.dimension_value(x.shape[-(nd + 1)]),
        index_points, self.kernel.feature_ndims)
    flat_num_index_points = tf.nest.flatten(num_index_points)
    static_non_singleton_num_points = set(
        n for n in flat_num_index_points if n is not None and n != 1)
    if len(static_non_singleton_num_points) > 1:
      raise ValueError(
          'Nested components of `index_points` must contain the same or '
          'broadcastable numbers of examples. Saw components with '
          f'{", ".join(list(str(n) for n in static_non_singleton_num_points))} '
          'examples.')
    if None in flat_num_index_points:
      warnings.warn(
          'Unable to detect statically whether the number of index_points is '
          '1. As a result, defaulting to treating the marginal GP at '
          '`index_points` as a multivariate Gaussian. This makes some methods, '
          'like `cdf` unavailable.')
    return all(n == 1 for n in flat_num_index_points)

  def _compute_covariance(self, index_points):
    kernel_matrix = self.kernel.matrix(index_points, index_points)
    if self._is_univariate_marginal(index_points):
      # kernel_matrix thus has shape [..., 1, 1]; squeeze off the last dims and
      # tack on the observation noise variance.
      return (tf.squeeze(kernel_matrix, axis=[-2, -1]) +
              self.observation_noise_variance)
    else:
      observation_noise_variance = tf.convert_to_tensor(
          self.observation_noise_variance)
      # We are compute K + obs_noise_variance * I. The shape of this matrix
      # is going to be a broadcast of the shapes of K and obs_noise_variance *
      # I.
      broadcast_shape = distribution_util.get_broadcast_shape(
          kernel_matrix,
          # We pad with two single dimension since this represents a batch of
          # scaled identity matrices.
          observation_noise_variance[..., tf.newaxis, tf.newaxis])

      kernel_matrix = tf.broadcast_to(kernel_matrix, broadcast_shape)
      return _add_diagonal_shift(
          kernel_matrix, observation_noise_variance[..., tf.newaxis])

  def get_marginal_distribution(self, index_points=None):
    """Compute the marginal of this GP over function values at `index_points`.

    Args:
      index_points: (nested) `Tensor` representing finite (batch of) vector(s)
        of points in the index set over which the GP is defined. Shape (or
        the shape of each nested component) has the form `[b1, ..., bB, e,
        f1, ..., fF]` where `F` is the number of feature dimensions and must
        equal `kernel.feature_ndims` (or its corresponding nested component)
        and `e` is the number (size) of index points in each batch.
        Ultimately this distribution corresponds to a `e`-dimensional
        multivariate normal. The batch shape must be broadcastable with
        `kernel.batch_shape` and any batch dims yielded by `mean_fn`.

    Returns:
      marginal: a Normal distribution with vector event shape, or (deprecated)
        a scalar `Normal` distribution if `index_points` consists of a single
        index point and `always_yield_multivariate_normal=False`.
    """
    with self._name_and_control_scope('get_marginal_distribution'):
      global _GET_MARGINAL_DISTRIBUTION_ALREADY_WARNED
      if (not _GET_MARGINAL_DISTRIBUTION_ALREADY_WARNED and  # pylint: disable=protected-access
          not self._always_yield_multivariate_normal):  # pylint: disable=protected-access
        warnings.warn(
            'When the `always_yield_multivariate_normal` arg to '
            '`GaussianProcess.__init__` is ignored, after 2023-02-15, '
            '`get_marginal_distribution` will always return a '
            'Normal distribution with vector event shape. This is the current '
            'behavior when `always_yield_multivariate_normal=True`. '
            'To recover the behavior of '
            '`always_yield_multivariate_normal=False` when `index_points` '
            'contains a single index point, build a scalar `Normal` '
            'distribution as follows: '
            '`mvn = get_marginal_distribution(index_points); `'
            '`norm = tfd.Normal(mvn.loc[..., 0], scale=mvn.stddev()[..., 0])`'
            '. To suppress these warnings, build the `GaussianProcess` with '
            '`always_yield_multivariate_normal=True`.',
            FutureWarning)
        _GET_MARGINAL_DISTRIBUTION_ALREADY_WARNED = True  # pylint: disable=protected-access
      return self._get_marginal_distribution(index_points=index_points)

  def _get_loc_and_covariance(
      self, index_points=None, is_missing=None, mask_loc=True):
    # TODO(cgs): consider caching the result here, keyed on `index_points`.
    index_points = self._get_index_points(index_points)
    covariance = self._compute_covariance(index_points)
    is_univariate_marginal = self._is_univariate_marginal(index_points)

    loc = self._mean_fn(index_points)
    if is_univariate_marginal:
      # `loc` has a trailing 1 in the shape; squeeze it.
      loc = tf.squeeze(loc, axis=-1)

    if is_missing is not None:
      if mask_loc:
        loc = tf.where(is_missing, 0., loc)
      if is_univariate_marginal:
        covariance = tf.where(is_missing, 1., covariance)
      else:
        covariance = psd_kernels_util.mask_matrix(covariance, is_missing)
    return loc, covariance

  def _get_marginal_distribution(self, index_points=None, is_missing=None):
    index_points = self._get_index_points(index_points)
    loc, covariance = self._get_loc_and_covariance(
        index_points=index_points, is_missing=is_missing)

    # If we're sure the number of index points is 1, we can just construct a
    # scalar Normal. This has computational benefits and supports things like
    # CDF that aren't otherwise straightforward to provide.
    if self._is_univariate_marginal(index_points):
      scale = tf.sqrt(covariance)
      return normal.Normal(
          loc=loc,
          scale=scale,
          validate_args=self._validate_args,
          allow_nan_stats=self._allow_nan_stats,
          name='marginal_distribution')
    else:
      return self._marginal_fn(
          loc=loc,
          covariance=covariance,
          validate_args=self._validate_args,
          allow_nan_stats=self._allow_nan_stats,
          name='marginal_distribution')

  @property
  def mean_fn(self):
    return self._mean_fn

  @property
  def kernel(self):
    return self._kernel

  @property
  def index_points(self):
    return self._index_points

  @property
  def observation_noise_variance(self):
    return self._observation_noise_variance

  @property
  def cholesky_fn(self):
    return self._cholesky_fn

  @property
  def marginal_fn(self):
    return self._marginal_fn

  @property
  @deprecation.deprecated(
      '2022-02-04',
      'the `jitter` property of `tfd.GaussianProcess` is deprecated; use the '
      '`marginal_fn` property instead.')
  def jitter(self):
    return self._jitter

  @classmethod
  def _parameter_properties(cls, dtype, num_classes=None):
    return dict(
        index_points=parameter_properties.ParameterProperties(
            event_ndims=lambda self: tf.nest.map_structure(  # pylint: disable=g-long-lambda
                lambda nd: nd + 1, self.kernel.feature_ndims),
            shape_fn=parameter_properties.SHAPE_FN_NOT_IMPLEMENTED,
        ),
        kernel=parameter_properties.BatchedComponentProperties(),
        observation_noise_variance=parameter_properties.ParameterProperties(
            event_ndims=0,
            shape_fn=lambda sample_shape: sample_shape[:-1],
            default_constraining_bijector_fn=(
                lambda: softplus_bijector.Softplus(low=dtype_util.eps(dtype)))))

  def _get_index_points(self, index_points=None):
    """Return `index_points` if not None, else `self._index_points`.

    Args:
      index_points: if given, this is what is returned; else,
      `self._index_points`

    Returns:
      index_points: the given arg, if not None, else the class member
      `self._index_points`.

    Rases:
      ValueError: if `index_points` and `self._index_points` are both `None`.
    """
    if self._index_points is None and index_points is None:
      raise ValueError(
          'This GaussianProcess instance was not instantiated with a value for '
          'index_points. One must therefore be provided when calling sample, '
          'log_prob, and other such methods. In particular, one can\'t compute '
          'KL divergences to/from an instance of `GaussianProccess` with '
          'unspecified `index_points` directly. Instead, use the '
          '`get_marginal_distribution` function, which takes `index_points` as '
          'an argument and returns a Normal distribution instance, whose KL '
          'can be computed.')
    return nest_util.convert_to_nested_tensor(
        index_points if index_points is not None else self._index_points,
        dtype_hint=self.kernel.dtype, allow_packing=True)

  @distribution_util.AppendDocstring(kwargs_dict={
      'index_points':
          'optional `float` `Tensor` representing a finite (batch of) of '
          'points in the index set over which this GP is defined. The shape '
          '(or shape of each nested component) has the form `[b1, ..., bB, e,'
          'f1, ..., fF]` where `F` is the ' 'number of feature dimensions and '
          'must equal ' '`self.kernel.feature_ndims` (or its corresponding '
          'nested component) and `e` is the number of index points in each '
          'batch. Ultimately, this distribution corresponds to an '
          '`e`-dimensional multivariate normal. The batch shape must be '
          'broadcastable with `kernel.batch_shape` and any batch dims yielded'
          'by `mean_fn`. If not specified, `self.index_points` is used. '
          'Default value: `None`.',
      'is_missing':
          'optional `bool` `Tensor` of shape `[..., e]`, where `e` is the '
          'number of index points in each batch.  Represents a batch of '
          'Boolean masks.  When `is_missing` is not `None`, the returned '
          'log-prob is for the *marginal* distribution, in which all '
          'dimensions for which `is_missing` is `True` have been marginalized '
          'out.  The batch dimensions of `is_missing` must broadcast with the '
          'sample and batch dimensions of `value` and of this `Distribution`. '
          'Default value: `None`.'
  })
  def _log_prob(self, value, index_points=None, is_missing=None):
    if is_missing is not None:
      is_missing = tf.convert_to_tensor(is_missing)
    value = tf.convert_to_tensor(value, dtype=self.dtype)
    index_points = self._get_index_points(index_points)
    loc, covariance = self._get_loc_and_covariance(
        index_points=index_points, is_missing=is_missing, mask_loc=False)

    if self._is_univariate_marginal(index_points):
      return _get_univariate_log_prob(
          loc=loc,
          covariance=covariance,
          value=value,
          dtype=self.dtype,
          is_missing=is_missing)

    event_shape = self._event_shape_tensor(index_points=index_points)

    return _get_multivariate_log_prob(
        loc=loc,
        covariance=covariance,
        value=value,
        event_shape=event_shape,
        dtype=self.dtype,
        cholesky_fn=self.cholesky_fn,
        marginal_fn=self.marginal_fn,
        is_missing=is_missing)

  def _event_shape_tensor(self, index_points=None):
    index_points = self._get_index_points(index_points)
    if self._is_univariate_marginal(index_points):
      return ps.constant([], dtype=tf.int32)
    else:
      # The examples index is one position to the left of the feature dims.
      example_shape = tf.nest.map_structure(
          lambda t, nd: ps.shape(t)[-(nd + 1):-nd],
          index_points, self.kernel.feature_ndims)
      return functools.reduce(ps.broadcast_shape,
                              tf.nest.flatten(example_shape), [])

  def _event_shape(self, index_points=None):
    index_points = (
        index_points if index_points is not None else self._index_points)
    if self._is_univariate_marginal(index_points):
      return tf.TensorShape([])
    else:
      # The examples index is one position to the left of the feature dims.
      example_shape = tf.nest.map_structure(
          lambda t, nd: tf.TensorShape(t.shape[-(nd + 1):-nd]),
          index_points, self.kernel.feature_ndims)
      flat_shapes = nest.flatten_up_to(self.kernel.feature_ndims, example_shape)

      if None in [tensorshape_util.rank(s) for s in flat_shapes]:
        return tf.TensorShape([None])
      return functools.reduce(
          tf.broadcast_static_shape, flat_shapes, tf.TensorShape([]))

  def _batch_shape(self, index_points=None):
    # TODO(b/249858459): Update `batch_shape_lib` so it can take override
    # parameters.
    result = batch_shape_lib.inferred_batch_shape(self)
    if index_points is not None:
      shapes = tf.nest.map_structure(
          lambda t, nd: t.shape[:-(nd + 1)],
          index_points, self.kernel.feature_ndims)
      flat_shapes = nest.flatten_up_to(self.kernel.feature_ndims, shapes)
      return functools.reduce(ps.broadcast_shape, flat_shapes, result)
    return result

  def _batch_shape_tensor(self, index_points=None):
    kwargs = {}
    if index_points is not None:
      kwargs = {'index_points': index_points}
    return batch_shape_lib.inferred_batch_shape_tensor(self, **kwargs)

  def _sample_n(self, n, seed=None, index_points=None):
    return self.get_marginal_distribution(index_points).sample(n, seed=seed)

  # Override to incorporate `index_points`
  def _set_sample_static_shape(self, x, sample_shape, index_points=None):
    """Helper to `sample`; sets static shape info."""
    batch_shape = self._batch_shape(index_points=index_points)
    event_shape = tf.TensorShape(self._event_shape(index_points=index_points))
    return distribution._set_sample_static_shape_for_tensor(  # pylint:disable=protected-access
        x,
        sample_shape=sample_shape,
        event_shape=event_shape,
        batch_shape=batch_shape)

  def _sample_and_log_prob(self,
                           sample_shape,
                           seed,
                           index_points=None,
                           **kwargs):
    return self.get_marginal_distribution(
        index_points).experimental_sample_and_log_prob(
            sample_shape, seed=seed, **kwargs)

  def _log_survival_function(self, value, index_points=None):
    return self.get_marginal_distribution(
        index_points).log_survival_function(value)

  def _survival_function(self, value, index_points=None):
    return self.get_marginal_distribution(index_points).survival_function(value)

  def _log_cdf(self, value, index_points=None):
    return self.get_marginal_distribution(index_points).log_cdf(value)

  def _entropy(self, index_points=None):
    return self.get_marginal_distribution(index_points).entropy()

  def _mean(self, index_points=None):
    index_points = self._get_index_points(index_points)
    mean = self._mean_fn(index_points)
    # We need to broadcast with the kernel hparams.
    batch_shape = self._batch_shape_tensor(index_points=index_points)
    event_shape = self._event_shape_tensor(index_points=index_points)
    if self._is_univariate_marginal(index_points):
      mean = tf.squeeze(mean, axis=-1)
    mean = tf.broadcast_to(mean, ps.concat([batch_shape, event_shape], axis=0))
    return mean

  def _quantile(self, value, index_points=None):
    return self.get_marginal_distribution(index_points).quantile(value)

  def _variance(self, index_points=None):
    index_points = self._get_index_points(index_points)

    kernel_diag = self.kernel.apply(index_points, index_points, example_ndims=1)
    if self._is_univariate_marginal(index_points):
      return (tf.squeeze(kernel_diag, axis=[-1]) +
              self.observation_noise_variance)
    else:
      # We are computing diag(K + obs_noise_variance * I) = diag(K) +
      # obs_noise_variance. We pad obs_noise_variance with a dimension in order
      # to broadcast batch shapes of kernel_diag and obs_noise_variance (since
      # kernel_diag has an extra dimension corresponding to the number of index
      # points).
      return kernel_diag + self.observation_noise_variance[..., tf.newaxis]

  def _covariance(self, index_points=None):
    # Using the result of get_marginal_distribution would involve an extra
    # matmul, and possibly even an unneceesary cholesky first. We can avoid that
    # by going straight through the kernel function.
    return self._compute_covariance(self._get_index_points(index_points))

  def _mode(self, index_points=None):
    return self.get_marginal_distribution(index_points).mode()

  def _default_event_space_bijector(self):
    return identity_bijector.Identity(validate_args=self.validate_args)

  def posterior_predictive(
      self, observations, predictive_index_points=None, **kwargs):
    """Return the posterior predictive distribution associated with this distribution.

    Returns the posterior predictive distribution `p(Y' | X, Y, X')` where:
      * `X'` is `predictive_index_points`
      * `X` is `self.index_points`.
      * `Y` is `observations`.

    This is equivalent to using the
    `GaussianProcessRegressionModel.precompute_regression_model` method.

    WARNING: This method assumes `index_points` is the only varying parameter
    (i.e. is a `Variable` / changes after initialization) and hence is not
    tape-safe.

    Args:
      observations: `float` `Tensor` representing collection, or batch of
        collections, of observations corresponding to
        `self.index_points`. Shape has the form `[b1, ..., bB, e]`, which
        must be broadcastable with the batch and example shapes of
        `self.index_points`. The batch shape `[b1, ..., bB]` must be
        broadcastable with the shapes of all other batched parameters
      predictive_index_points: (nested) `Tensor` representing finite collection,
        or batch of collections, of points in the index set over which the GP
        is defined. Shape (or shape of each nested component) has the form
        `[b1, ..., bB, e, f1, ..., fF]` where `F` is the number of feature
        dimensions and must equal `kernel.feature_ndims` (or its
        corresponding nested component) and `e` is the number (size) of
        predictive index points in each batch. The batch shape must be
        broadcastable with this distributions `batch_shape`.
        Default value: `None`.
      **kwargs: Any other keyword arguments to pass / override.

    Returns:
      gprm: An instance of `Distribution` that represents the posterior
        predictive.
    """
    from tensorflow_probability.substrates.numpy.distributions import gaussian_process_regression_model as gprm  # pylint:disable=g-import-not-at-top
    if self.index_points is None:
      raise ValueError(
          'Expected that `self.index_points` is not `None`. Using '
          '`self.index_points=None` is equivalent to using a `GaussianProcess` '
          'prior, which this class encapsulates.')
    argument_dict = {
        'kernel': self.kernel,
        'observation_index_points': self.index_points,
        'observations': observations,
        'index_points': predictive_index_points,
        'observation_noise_variance': self.observation_noise_variance,
        'cholesky_fn': self.cholesky_fn,
        'mean_fn': self.mean_fn,
        'jitter': self.jitter,
        'always_yield_multivariate_normal':
            self._always_yield_multivariate_normal,
        'validate_args': self.validate_args,
        'allow_nan_stats': self.allow_nan_stats
    }
    argument_dict.update(**kwargs)

    return gprm.GaussianProcessRegressionModel.precompute_regression_model(
        **argument_dict)

  @property
  def _type_spec(self):
    return _GaussianProcessTypeSpec.from_instance(
        self,
        omit_kwargs=('parameters', '_check_marginal_cholesky_fn'),
        non_identifying_kwargs=('name',))

  def _convert_variables_to_tensors(self):
    return auto_composite_tensor.convert_variables_to_tensors(self)

  def __repr__(self):
    if self.index_points is None:
      event_shape_str = '?'
    else:
      event_shape_str = distribution._str_tensorshape(self.event_shape)
    return ('<tfp.distributions.{type_name} '
            '\'{self_name}\''
            ' batch_shape={batch_shape}'
            ' event_shape={event_shape}'
            ' dtype={dtype}>'.format(
                type_name=type(self).__name__,
                self_name=self.name or '<unknown>',
                batch_shape=distribution._str_tensorshape(self.batch_shape),
                event_shape=event_shape_str,
                dtype=distribution._str_dtype(self.dtype)))


@auto_composite_tensor.type_spec_register(
    'tfp.distributions.GaussianProcess_ACTTypeSpec')
class _GaussianProcessTypeSpec(
    auto_composite_tensor._AutoCompositeTensorTypeSpec):  # pylint: disable=protected-access
  """TypeSpec for GaussianProcess."""

  @property
  def value_type(self):
    return GaussianProcess

  def _from_components(self, components):
    # Disable the check that at most one of `marginal_fn` and `cholesky_fn` is
    # passed to the constructor, since both may have been set internally.
    components['_check_marginal_cholesky_fn'] = False
    return super(_GaussianProcessTypeSpec, self)._from_components(components)


def _get_univariate_log_prob(
    loc, covariance, value, dtype, is_missing=None):
  """Compute GP logprob over one index point."""
  value = value - loc
  log_normalizer_constant = dtype_util.as_numpy_dtype(
      value.dtype)(np.log(2. * np.pi))
  if is_missing is not None:
    value = tf.where(is_missing, 0., value)
  lp = -0.5 * (tf.math.square(value) / covariance +
               tf.math.log(covariance) +
               log_normalizer_constant)
  if is_missing is not None:
    num_masked_dims = tf.cast(is_missing, dtype)
    lp = lp + 0.5 * log_normalizer_constant * num_masked_dims
  return lp


def _get_multivariate_log_prob(
    loc, covariance, value,
    event_shape, dtype,
    cholesky_fn=None,
    marginal_fn=None,
    is_missing=None):
  """Compute GP logprob over multiple index points."""
  # Use marginal_fn if cholesky_fn doesn't exist.
  log_normalizer_constant = dtype_util.as_numpy_dtype(dtype)(np.log(2. * np.pi))
  half = dtype_util.as_numpy_dtype(dtype)(0.5)

  if cholesky_fn is None:
    if is_missing is not None:
      loc = tf.where(is_missing, 0., loc)
      value = tf.where(is_missing, 0., value)
    lp = marginal_fn(
        loc=loc,
        covariance=covariance,
        name='marginal_distribution').log_prob(value)
  else:
    value = value - loc
    if is_missing is not None:
      value = tf.where(is_missing, 0., value)
    chol_covariance = cholesky_fn(covariance)
    lp = -0.5 * (
        linalg.hpsd_quadratic_form_solvevec(
            covariance, value, cholesky_matrix=chol_covariance) +
        linalg.hpsd_logdet(covariance, cholesky_matrix=chol_covariance))
    lp = lp - (half * log_normalizer_constant * tf.cast(event_shape[-1], dtype))

  if is_missing is not None:
    num_masked_dims = tf.cast(tf.math.count_nonzero(is_missing, axis=-1), dtype)
    lp = lp + half * log_normalizer_constant * num_masked_dims
  return lp


def _assert_kl_compatible(marginal, other):
  if ((isinstance(marginal, normal.Normal) and
       isinstance(other, normal.Normal)) or
      (isinstance(marginal,
                  mvn_linear_operator.MultivariateNormalLinearOperator) and
       isinstance(other,
                  mvn_linear_operator.MultivariateNormalLinearOperator))):
    return
  raise ValueError(
      'Attempting to compute KL between a GP marginal and a distribution of '
      'incompatible type. GP marginal has type {} and other distribution has '
      'type {}.'.format(type(marginal), type(other)))


def _kl_gp_compatible(gp, compatible, name):
  with tf.name_scope(name):
    marginal = gp.get_marginal_distribution()
    _assert_kl_compatible(marginal, compatible)
    return kullback_leibler.kl_divergence(marginal, compatible)


def _kl_compatible_gp(compatible, gp, name):
  with tf.name_scope(name):
    marginal = gp.get_marginal_distribution()
    _assert_kl_compatible(marginal, compatible)
    return kullback_leibler.kl_divergence(compatible, marginal)


@kullback_leibler.RegisterKL(GaussianProcess, normal.Normal)
def _kl_gp_normal(gp, n, name=None):
  """Calculate the batched KL divergence KL(gp || n).

  Args:
    gp: instance of a GaussianProcess distribution object.
    n: instance of a Normal distribution object.
    name: (optional) Name to use for created operations.
      default is 'kl_gp_normal'.

  Returns:
    Batchwise KL(gp || n)
  """
  return _kl_gp_compatible(gp, n, name or 'kl_gp_normal')


@kullback_leibler.RegisterKL(
    GaussianProcess, mvn_linear_operator.MultivariateNormalLinearOperator)
def _kl_gp_mvn(gp, mvn, name=None):
  """Calculate the batched KL divergence KL(gp || mvn).

  Args:
    gp: instance of a GaussianProcess distribution object.
    mvn: instance of a multivariate Normal distribution object (any subclass of
      MultivariateNormalLinearOperator)
    name: (optional) Name to use for created operations.
      default is 'kl_gp_mvn'.

  Returns:
    Batchwise KL(gp || mvn)
  """
  return _kl_gp_compatible(gp, mvn, name or 'kl_gp_mvn')


@kullback_leibler.RegisterKL(normal.Normal, GaussianProcess)
def _kl_normal_gp(n, gp, name=None):
  """Calculate the batched KL divergence KL(gp || n).

  Args:
    n: instance of a Normal distribution object.
    gp: instance of a GaussianProcess distribution object.
    name: (optional) Name to use for created operations.
      default is 'kl_normal_gp'.

  Returns:
    Batchwise KL(n || gp)
  """
  return _kl_compatible_gp(n, gp, name or 'kl_normal_gp')


@kullback_leibler.RegisterKL(
    mvn_linear_operator.MultivariateNormalLinearOperator, GaussianProcess)
def _kl_mvn_gp(mvn, gp, name=None):
  """Calculate the batched KL divergence KL(mvn || gp).

  Args:
    mvn: instance of a multivariate Normal distribution object (any subclass of
      MultivariateNormalLinearOperator)
    gp: instance of a GaussianProcess distribution object.
    name: (optional) Name to use for created operations.
      default is 'kl_mvn_gp'.

  Returns:
    Batchwise KL(mvn || gp)
  """
  return _kl_compatible_gp(mvn, gp, name or 'kl_mvn_gp')


def _pytree_unflatten(aux_data, children):
  keys, metadata = aux_data
  non_tensor_params = metadata['non_tensor_params']
  non_tensor_params['_check_marginal_cholesky_fn'] = False
  parameters = dict(list(zip(keys, children)),
                    **non_tensor_params,
                    **metadata['callable_params'])
  return GaussianProcess(**parameters)


if JAX_MODE:
  from jax import tree_util  # pylint: disable=g-import-not-at-top
  tree_util.register_pytree_node(
      GaussianProcess,
      auto_composite_tensor.pytree_flatten,
      _pytree_unflatten)


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# This file is auto-generated by substrates/meta/rewrite.py
# It will be surfaced by the build system as a symlink at:
#   `tensorflow_probability/substrates/numpy/distributions/gaussian_process.py`
# For more info, see substrate_runfiles_symlinks in build_defs.bzl
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
