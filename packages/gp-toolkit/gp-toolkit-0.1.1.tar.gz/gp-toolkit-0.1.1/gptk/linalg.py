import tensorflow as tf


def tril_solve(tril: tf.Tensor, rhs: tf.Tensor, *args, **kwargs):
    """
    Solve systems of linear equations with lower triangular matrices.
    """
    return tf.linalg.triangular_solve(tril, rhs, lower=True, *args, **kwargs)


def cho_solve_from_tril_solve(tril: tf.Tensor, tril_inv_rhs: tf.Tensor):
    """
    Solve system of linear equations `(LL^T) X = B` given `L` and `L^{-1} B`,
    i.e. the solution to the systems of linear equations `L X = B` with lower
    triangular matrix L.

    Note the X that satisfies `L^T X = L^{-1} B` trivially
    satisfies `(LL^T) X = B`.
    """
    return tril_solve(tril, tril_inv_rhs, adjoint=True)


def gramian(a, b=None, diag: bool = True):
    """
    Computes A^H @ B.
    """
    if b is None:
        b = a
    return tf.reduce_sum(a * b, axis=-2) if diag \
        else tf.linalg.matmul(a, b, adjoint_a=True)
