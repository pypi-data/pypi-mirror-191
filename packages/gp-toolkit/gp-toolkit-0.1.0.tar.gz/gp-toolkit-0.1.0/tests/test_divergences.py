#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from gpflow.base import TensorType, Parameter
from gpflow.kernels import Kernel, SquaredExponential
from gpflow.inducing_variables import InducingVariables, InducingPoints
from gpflow.covariances import Kuu
from gpflow.kullback_leiblers import prior_kl, gauss_kl
from gpflow.utilities import positive, triangular
from gpflow.config import default_float, default_jitter

from gptk.divergences.base import _base_kl_divergence_linop
from gptk.conditionals.utils import create_linear_operator_pd

tfd = tfp.distributions


@pytest.mark.parametrize("white", [False, True])
def test(Kmm, q_loc, q_scale_linop, white):

    if white:
        Kmm_linop = create_linear_operator_pd(Kmm)
        Lm_linop = Kmm_linop.cholesky()
        L = Lm_linop.to_dense()
    else:
        L = Lm_linop = None

    q_mu = tf.transpose(q_loc)  # [M, P]
    if isinstance(q_scale_linop, tf.linalg.LinearOperatorDiag):
        q_sqrt = tf.transpose(q_scale_linop.diag_part())  # [M, P]
    else:
        q_sqrt = q_scale_linop.to_dense()  # [P, M, M]

    kl_1 = _base_kl_divergence_linop(q_loc, q_scale_linop, Lm_linop)
    kl_2 = gauss_kl(q_mu, q_sqrt, K_cholesky=L)

    np.testing.assert_approx_equal(kl_1, kl_2)
