from typing import Optional

import tensorflow as tf
import tensorflow_probability as tfp

from gpflow.kernels import Kernel
from gpflow.inducing_variables import InducingVariables
from gpflow.covariances.kuus import Kuu
from gpflow.kullback_leiblers import prior_kl
from gpflow.config import default_jitter

from ..inducing_variables.base import InducingPointsExtended

tfd = tfp.distributions


@prior_kl.register(InducingPointsExtended, Kernel, object, tf.linalg.LinearOperator)
def _prior_kl_divergence_linop(inducing_variable, kernel, q_loc, q_scale_linop, whiten):
    if whiten:
        Lm_linop = None
    else:
        Kmm_linop = Kuu(inducing_variable, kernel, jitter=default_jitter())
        Lm_linop = Kmm_linop.cholesky()
    return _base_kl_divergence_linop(q_loc, q_scale_linop, Lm_linop)


def _get_variational_distribution(loc: tf.Tensor, scale_linop: tf.linalg.LinearOperator):
    if isinstance(scale_linop, tf.linalg.LinearOperatorLowerTriangular):
        q = tfd.MultivariateNormalTriL(loc, scale_tril=scale_linop.tril)
    elif isinstance(scale_linop, tf.linalg.LinearOperatorDiag):
        q = tfd.MultivariateNormalDiag(loc, scale_diag=scale_linop.diag)
    else:
        q = tfd.MultivariateNormalLinearOperator(loc, scale_linop)
    return q


def _base_kl_divergence_linop(
        q_loc: tf.Tensor, q_scale_linop: tf.linalg.LinearOperator, 
        p_scale_linop: Optional[tf.linalg.LinearOperatorLowerTriangular] = None):

    # p: batch_shape=[], event_shape=[M]
    if p_scale_linop is None:
        p = tfd.MultivariateNormalDiag(scale_diag=tf.ones_like(q_loc[-1]))
    else:
        # p = tfd.MultivariateNormalTriL(scale_tril=p_scale_linop.tril)
        p = tfd.MultivariateNormalLinearOperator(scale=p_scale_linop)

    # q: batch_shape=[P], event_shape=[M]
    q = _get_variational_distribution(q_loc, q_scale_linop)

    kl_batch = tfd.kl_divergence(q, p)  # shape=[P]
    return tf.reduce_sum(kl_batch, axis=None)
