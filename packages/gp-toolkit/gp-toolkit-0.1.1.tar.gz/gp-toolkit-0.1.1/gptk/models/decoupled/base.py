import tensorflow as tf

from ...conditionals.utils import compute_projections, adjoint_scale_mvn
from ...linalg import gramian


# Knn: tf.Tensor, Kmn: tf.Tensor, Kkn: tf.Tensor,
#                      Kmm: tf.Tensor, Kmk: tf.Tensor, Kkk: tf.Tensor,
#                      g_loc, g_scale, h_loc, h_scale,
#                      g_scale_diag, h_scale_diag,
#                      g_whiten: bool = True, h_whiten: bool = True,
#                      diag_cov: bool = True

def _base_conditional_linop(
        Kmm_linop: tf.linalg.LinearOperator,
        Kmn: tf.Tensor, Knn: tf.Tensor, Kkn: tf.Tensor,
        Kmk: tf.Tensor, Kkk: tf.Tensor,
        q_loc: tf.Tensor, q_scale_linop: tf.linalg.LinearOperator,
        white: bool, diag_cov: bool):

    Lm_linop = Kmm_linop.cholesky()  # LinearOperatorLowerTriangular; [M, M]
    Lm_inv_Kmn = Lm_linop.solve(Kmn)  # Tensor; [M, N]

    # Qnn, Qmn = compute_projections(Lm_linop, Lm_inv_Kmn, white, diag_cov=diag_cov)  # [N, N], [M, N]
    # mean, cov = adjoint_scale_mvn(Qmn, q_loc, q_scale_linop, diag_cov=diag_cov)  # [P, N], [P, N] or [P, N, N]
    # cov += Knn - Qnn

    # Lm = tf.linalg.cholesky(Kmm)  # [M, M]
    # Lm_inv_Kmn = tril_solve(Lm, Kmn)  # [M, N]

    Lm_inv_Kmk = Lm_linop.solve(Kmk)  # Tensor; [M, K]

    Qkk = gramian(Lm_inv_Kmk, diag=False)  # Tensor; [K, K]

    # Ckk = Kkk - Qkk  # Tensor; [K, K]
    Ckk_linop = create_linear_operator_pd(Kkk - Qkk)
    # Lk = tf.linalg.cholesky(Ckk)   # [K, K]
    Lk_linop = Ckk_linop.cholesky()

    # Lk, Lm_inv_Kmk = _get_schur_complement_chol(Lm, Kkk, Kmk)  # [K, K], [M, K]

    Qkn = gramian(Lm_inv_Kmk, Lm_inv_Kmn, diag=False)  # [K, N]
    Ckn = Kkn - Qkn  # [K, N]

    # Lk_inv_Ckn = tril_solve(Lk, Ckn)  # [K, N]

    Lk_inv_Ckn = Lk_linop.solve(Ckn)

    Qnn, Qmn = compute_projections(Lm_linop, Lm_inv_Kmn, white, diag_cov=diag_cov)  # [N, N], [M, N]
    Rnn, Rkn = compute_projections(Lk_linop, Lk_inv_Ckn, white, diag_cov=diag_cov)  # [N, N], [K, N]
    # Cnn = Knn - Qnn

    # print(f"g_scale: {g_scale}, h_scale {h_scale}")
    # [R, N], [R, N] if diag_cov else [R, N, N]
    # g_mu, g_Sigma = adjoint_scale_mvn(g_loc, g_scale, Qmn, diag_cov, g_scale_diag)
    # h_mu, h_Sigma = adjoint_scale_mvn(h_loc, h_scale, Rkn, diag_cov, h_scale_diag)

    mean, cov = adjoint_scale_mvn(Qmn, q_loc, q_scale_linop, diag_cov=diag_cov)  # [P, N], [P, N] or [P, N, N]
    h_mean, h_cov = adjoint_scale_mvn(Rkn, q_loc, q_scale_linop, diag_cov=diag_cov)  # [P, N], [P, N] or [P, N, N]

    mean += h_mean
    cov += h_cov

    cov += Knn - Qnn - Rnn

    return mean, cov
