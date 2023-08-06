import logging
import tensorflow as tf

from gpflow.kernels import Kernel, MultioutputKernel
from gpflow.covariances import Kuu

from ..conditionals.utils import create_linear_operator_pd
from ..inducing_variables.base import InducingPointsExtended


logger = logging.getLogger(__name__)


@Kuu.register(InducingPointsExtended, Kernel)
def _Kuu_linop(inducing_variable, kernel, *, jitter=0.0):

    logger.debug("Calling an alternative implementation of Kuu() "
                 "modded by gp-toolkit.")

    Kzz = kernel(inducing_variable.Z)
    Kzz += jitter * tf.eye(inducing_variable.num_inducing, dtype=Kzz.dtype)
    return create_linear_operator_pd(Kzz)


@Kuu.register(InducingPointsExtended, MultioutputKernel)
def _Kuu_linop_multioutput(inducing_variable, kernel, *, jitter=0.0):
    raise NotImplementedError("Not yet supported!")
