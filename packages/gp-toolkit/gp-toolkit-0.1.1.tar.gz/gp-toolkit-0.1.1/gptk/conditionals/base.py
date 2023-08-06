"""Main module."""
import logging
import tensorflow as tf

from gpflow.kernels import Kernel, MultioutputKernel
from gpflow.inducing_variables import InducingVariables
from gpflow.covariances import Kuu, Kuf
from gpflow.conditionals import conditional
from gpflow.conditionals.util import base_conditional, expand_independent_outputs
from gpflow.config import default_jitter

from ..inducing_variables.base import InducingPointsExtended
from ..linalg import tril_solve
from .utils import compute_projections, adjoint_scale_mvn

logger = logging.getLogger(__name__)


def _base_conditional_linop(
        Kmm_linop: tf.linalg.LinearOperator,
        Kmn: tf.Tensor, Knn: tf.Tensor,
        q_loc: tf.Tensor, q_scale_linop: tf.linalg.LinearOperator,
        white: bool, diag_cov: bool):

    Lm_linop = Kmm_linop.cholesky()  # LinearOperatorLowerTriangular; [M, M]
    Lm_inv_Kmn = Lm_linop.solve(Kmn)  # Tensor; [M, N]

    Qnn, Qmn = compute_projections(Lm_linop, Lm_inv_Kmn, white, diag_cov=diag_cov)  # [N, N], [M, N]
    mean, cov = adjoint_scale_mvn(Qmn, q_loc, q_scale_linop, diag_cov=diag_cov)  # [P, N], [P, N] or [P, N, N]
    cov += Knn - Qnn

    return mean, cov


def _base_conditional_linop_compat(
        Kmm_linop: tf.linalg.LinearOperator,
        Kmn: tf.Tensor, Knn: tf.Tensor,
        q_loc: tf.Tensor, q_scale_linop: tf.linalg.LinearOperator,
        white: bool, diag_cov: bool):

    meanT, covT = _base_conditional_linop(Kmm_linop, Kmn, Knn, q_loc, q_scale_linop, white, diag_cov)

    mean = tf.transpose(meanT)
    cov = tf.transpose(covT) if diag_cov else covT

    return mean, cov


@conditional.register(object, InducingPointsExtended, Kernel, object)
def _conditional(
    Xnew,
    inducing_variable,
    kernel,
    f,
    *,
    full_cov=False,
    full_output_cov=False,
    q_sqrt=None,
    white=False,
):

    logger.debug("Calling a modded version of conditional() "
                 "provided by gp-toolkit.")

    diag_cov = not full_cov

    Knn = kernel(Xnew, full_cov=full_cov)
    Kmm = Kuu(inducing_variable, kernel, jitter=default_jitter())  # [M, M]
    Kmn = Kuf(inducing_variable, kernel, Xnew)  # [M, N]

    mean, cov = _base_conditional_linop_compat(Kmm, Kmn, Knn, f, q_sqrt, white, diag_cov)

    # return mean, expand_independent_outputs(cov, full_cov, full_output_cov)
    return mean, cov


@conditional.register(object, InducingPointsExtended, MultioutputKernel, object)
def _conditional_multioutput(inducing_variable, kernel, *, jitter=0.0):
    raise NotImplementedError("Not yet supported!")
