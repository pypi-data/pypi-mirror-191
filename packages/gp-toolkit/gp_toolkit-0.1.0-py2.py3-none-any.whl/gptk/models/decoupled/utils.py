import tensorflow as tf

from ..linalg import tril_solve, _adjoint_matmul
from ..conditionals.utils import adjoint_scale_mvn, projection


def predictive_terms(Knn: tf.Tensor, Kmn: tf.Tensor, Kkn: tf.Tensor,
                     Kmm: tf.Tensor, Kmk: tf.Tensor, Kkk: tf.Tensor,
                     g_loc, g_scale, h_loc, h_scale,
                     g_scale_diag, h_scale_diag,
                     g_whiten: bool = True, h_whiten: bool = True,
                     diag_cov: bool = True):

    (Qnn, Qmn), (Rnn, Rkn) = _get_coefficients(Kmn, Kkn, Kmm, Kmk, Kkk,
                                               g_whiten, h_whiten, diag_cov)

    # print(f"g_scale: {g_scale}, h_scale {h_scale}")
    # [R, N], [R, N] if diag_cov else [R, N, N]
    g_mu, g_Sigma = adjoint_scale_mvn(g_loc, g_scale, Qmn, diag_cov, g_scale_diag)
    h_mu, h_Sigma = adjoint_scale_mvn(h_loc, h_scale, Rkn, diag_cov, h_scale_diag)

    return [g_mu, h_mu], [[g_Sigma], [Knn, -Qnn, -Rnn, h_Sigma]]


def _get_schur_complement_chol(Lm, Kkk, Kmk):
    """
    Get the Cholesky decomposition of the Schur complement of block `Kmm` in
    matrix
        [ Kkk Kkm ]
        [ Kmk Kmm ]
    given `Kkk`, `Kmk`, and `Lm` where Lm Lm^T = Kmm.

    The Schur complement is
        Ckk = Kkk - Kkm Kmm^{-1} Kmk = Kkk - (Kkm Lm^{-T}) (Lm^{-1} Kmk)
    Returns the Cholesky decomposition Lk where Lk Lk^T = Ckk
    and Lm^{-1} Kmk (for subsequent re-use to avoid extraneous O(M^3) time
    computations).
    """
    Lm_inv_Kmk = tril_solve(Lm, Kmk)  # [M, K]
    Qkk = _adjoint_matmul(Lm_inv_Kmk, diag=False)  # [K, K]
    Ckk = Kkk - Qkk  # [K, K]
    Lk = tf.linalg.cholesky(Ckk)   # [K, K]
    return Lk, Lm_inv_Kmk


def _get_coefficients(Kmn: tf.Tensor, Kkn: tf.Tensor,
                      Kmm: tf.Tensor, Kmk: tf.Tensor, Kkk: tf.Tensor,
                      g_whiten, h_whiten, diag_cov):

    # TODO(LT): Think of a more descriptive name.

    Lm = tf.linalg.cholesky(Kmm)  # [M, M]
    Lm_inv_Kmn = tril_solve(Lm, Kmn)  # [M, N]

    Lk, Lm_inv_Kmk = _get_schur_complement_chol(Lm, Kkk, Kmk)  # [K, K], [M, K]

    Qkn = _adjoint_matmul(Lm_inv_Kmk, Lm_inv_Kmn, diag=False)  # [K, N]
    Ckn = Kkn - Qkn  # [K, N]

    Lk_inv_Ckn = tril_solve(Lk, Ckn)  # [K, N]

    Qnn, Qmn = projection(Lm, Lm_inv_Kmn, g_whiten, diag_cov)  # [N, N], [M, N]
    Rnn, Rkn = projection(Lk, Lk_inv_Ckn, h_whiten, diag_cov)  # [N, N], [K, N]

    return (Qnn, Qmn), (Rnn, Rkn)
