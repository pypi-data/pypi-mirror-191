import tensorflow as tf
import logging

from ..linalg import gramian


logger = logging.getLogger(__name__)


def create_linear_operator_pd(matrix: tf.Tensor) -> tf.linalg.LinearOperator:
    return tf.linalg.LinearOperatorFullMatrix(matrix,
                                              is_self_adjoint=True,
                                              is_positive_definite=True)


def adjoint_scale_mvn(adjoint: tf.Tensor,
                      loc: tf.Tensor, scale_linop: tf.linalg.LinearOperator,
                      diag_cov: bool):
    """
    Given m and L representing multivariate normal random variable 
        u ~ N(m, LL^T),
    calculate the mean and covariance of the transformed variable A^T u given 
    matrix A, which are simply
      A^T m,    and     A^T (LL^T) A = (L^T A)^T L^T A,
    respectively.

    In probabilistic programming terms, equivalent to transforming the
    multivariate normal distribution 
    `tfd.MultivariateNormalLinearOperator(loc, scale_linop)` by the bijector
    `tfp.bijectors.ScaleMatvecLinearOperator(adjoint_linop, adjoint=True)`.

    Parameters
    ----------
    adjoint : tf.Tensor
        The (adjoint) matrix by which to transform `loc` and `scale`. 
        The shape is `[..., M, N]`.
    loc : tf.Tensor
        The location vector of shape `[..., M]`.
    scale_linop : tf.linalg.LinearOperator
        The scale matrix (Cholesky factor of the covariance matrix).
    diag_cov : bool

    Returns
    -------
    loc_new : Tensor
        The transformed location of shape `[..., M]`.
    cov_new : Tensor
        The covariance matrix corresponding to the transformed scale.
        Shape is `[..., M]` if `diag_cov`, otherwise `[..., M, M]`.
    """
    # [..., M] [..., M, N] -> [..., N]
    loc_new = tf.linalg.matvec(adjoint, loc, adjoint_a=True)

    # [..., M, M] [..., M, N] -> [..., M, N]
    scale_new = scale_linop.matmul(adjoint, adjoint=True)

    # [..., N, M] [..., M, N] -> [..., N, N] or [..., N]
    cov_new = gramian(scale_new, diag=diag_cov)

    return loc_new, cov_new


def compute_projections(Lm_linop: tf.linalg.LinearOperatorLowerTriangular, 
                        Lm_inv_Kmn: tf.Tensor, white: bool, diag_cov: bool):
    """
    Get Nystroem approximation (to Knn) and the matrix scale / coefficient.

    Qnn = Knm Kmm^{-1} Kmn = (Knm Lm^{-T}) (Lm^{-1} Kmn)
    Qmn = Lm^{-1} Kmn if whiten else Kmm^{-1} Kmn = Lm^{-T} (Lm^{-1} Kmn)
    """
    Qnn = gramian(Lm_inv_Kmn, diag=diag_cov)
    Qmn = Lm_inv_Kmn if white else Lm_linop.solve(Lm_inv_Kmn, adjoint=True)
    return Qnn, Qmn
