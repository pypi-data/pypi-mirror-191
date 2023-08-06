import tensorflow as tf
import numpy as np

from ..inducing_variables import InducingPointsExtended

from gpflow.base import Parameter, TensorLike
from gpflow.kernels import Matern32
from gpflow.covariances import Kuu, Kuf
from gpflow.utilities import to_default_float
from gpflow.config import default_float


class FourierFeatures1D(InducingPointsExtended):

    def __init__(self, start, end, n_components):
        """
        `a` and `b` define the interval [a, b] of the Fourier representation.
        `M` specifies the number of frequencies to use.
        """
        # [a, b] defining the interval of the Fourier representation:
        self.start = Parameter(start, dtype=default_float())
        self.end = Parameter(end, dtype=default_float())
        self.n_components = n_components
        # integer array defining the frequencies, ω_m = 2π (b - a)/m:
        self.components = np.arange(n_components)

    @property
    def num_inducing(self):
        """ number of inducing variables (defines dimensionality of q(u)) """
        return 2 * self.n_components - 1  # `M` cosine and `M-1` sine components


@Kuu.register(FourierFeatures1D, Matern32)
def Kuu_matern32_fourierfeatures1d(inducing_variable, kernel, jitter=None):
    a, b, ms = (lambda u: (u.start, u.end, u.components))(inducing_variable)
    omegas = 2.0 * np.pi * ms / (b - a)

    # Cosine block: eq. (114)
    lamb = np.sqrt(3.0) / kernel.lengthscales
    four_or_eight = to_default_float(tf.where(omegas == 0, 4.0, 8.0))
    d_cos = (
        (b - a)
        * tf.square(tf.square(lamb) + tf.square(omegas))
        / tf.pow(lamb, 3)
        / kernel.variance
        / four_or_eight
    )
    v_cos = tf.ones_like(d_cos) / tf.sqrt(kernel.variance)
    cosine_block = tf.linalg.LinearOperatorLowRankUpdate(tf.linalg.LinearOperatorDiag(d_cos, is_positive_definite=True), v_cos[:, None])

    # Sine block: eq. (115)
    omegas = omegas[tf.not_equal(omegas, 0)]  # don't compute omega=0
    d_sin = (
        (b - a)
        * tf.square(tf.square(lamb) + tf.square(omegas))
        / tf.pow(lamb, 3)
        / kernel.variance
        / 8.0
    )
    v_sin = omegas / lamb / tf.sqrt(kernel.variance)
    sine_block = tf.linalg.LinearOperatorLowRankUpdate(tf.linalg.LinearOperatorDiag(d_sin, is_positive_definite=True), v_sin[:, None])

    return tf.linalg.LinearOperatorBlockDiag([cosine_block, sine_block])  # eq. (116)


@Kuf.register(FourierFeatures1D, Matern32, TensorLike)
def Kuf_matern32_fourierfeatures1d(inducing_variable, kernel, X):
    X = tf.squeeze(X, axis=1)
    a, b, ms = (lambda u: (u.start, u.end, u.components))(inducing_variable)
    omegas = 2.0 * np.pi * ms / (b - a)

    Kuf_cos = tf.cos(omegas[:, None] * (X[None, :] - a))
    omegas_sin = omegas[tf.not_equal(omegas, 0)]  # don't compute zeros freq.
    Kuf_sin = tf.sin(omegas_sin[:, None] * (X[None, :] - a))

    # correct Kuf outside [a, b] -- see Table 1

    def tail_cos(delta_X):
        arg = np.sqrt(3) * tf.abs(delta_X) / kernel.lengthscales
        return (1 + arg) * tf.exp(-arg)[None, :]

    Kuf_cos = tf.where(X < a, tail_cos(X - a), Kuf_cos)
    Kuf_cos = tf.where(X > b, tail_cos(X - b), Kuf_cos)

    def tail_sin(delta_X):
        arg = np.sqrt(3) * tf.abs(delta_X) / kernel.lengthscales
        return delta_X[None, :] * tf.exp(-arg) * omegas_sin[:, None]

    Kuf_sin = tf.where(X < a, tail_sin(X - a), Kuf_sin)
    Kuf_sin = tf.where(X > b, tail_sin(X - b), Kuf_sin)

    return tf.concat([Kuf_cos, Kuf_sin], axis=0)
