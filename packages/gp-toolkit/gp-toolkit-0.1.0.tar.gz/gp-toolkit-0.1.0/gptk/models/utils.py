import tensorflow as tf

from gpflow.base import Parameter
from gpflow.utilities import positive, triangular
from gpflow.config import default_float

from tensorflow.keras.initializers import get as get_initializer, Ones
from ..initializers import Identity


def create_variational_loc(output_dim, n_inducing, initializer):
    initializer = get_initializer(initializer)
    initial_value = initializer(shape=(output_dim, n_inducing))  # [P, M]
    return Parameter(initial_value, dtype=default_float())


def create_variational_scale(output_dim, n_inducing, diag, initializer=None):

    initializer = get_initializer(initializer)

    if diag:

        assert not isinstance(initializer, Identity), \
            "Initializer `Identity` not defined for diagonal " \
            "variational scale parameter!"

        if initializer is None:
            initializer = Ones()

        # [P, M]
        initial_value = initializer(shape=(output_dim, n_inducing),
                                    dtype=default_float())

        scale = Parameter(initial_value, transform=positive())
        scale_linop = tf.linalg.LinearOperatorDiag(diag=scale)
    else:

        if initializer is None:
            initializer = Identity()

        # [P, M, M]
        initial_value = initializer(shape=(output_dim, n_inducing, n_inducing),
                                    dtype=default_float())

        scale = Parameter(initial_value, transform=triangular())
        scale_linop = tf.linalg.LinearOperatorLowerTriangular(tril=scale)

    return scale_linop
