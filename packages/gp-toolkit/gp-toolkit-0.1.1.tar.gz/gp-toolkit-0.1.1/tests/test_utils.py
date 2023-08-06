#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from gptk.conditionals.utils import adjoint_scale_mvn

tfd = tfp.distributions


@pytest.fixture
def adjoint(n_inducing, n_test, random_state):    
    return random_state.randn(n_inducing, n_test)  # [M, N]


@pytest.mark.parametrize("diag_cov", [False, True])
def test_adjoint_scale_mvn(adjoint, q_loc, q_scale_linop, diag_cov):

    loc_new, cov_new = adjoint_scale_mvn(adjoint, q_loc, q_scale_linop, diag_cov)

    linop_adjoint = tf.linalg.LinearOperatorFullMatrix(adjoint)
    # linop = tf.linalg.LinearOperatorAdjoint(linop_adjoint)

    bijector = tfp.bijectors.ScaleMatvecLinearOperator(linop_adjoint, adjoint=True)
    # bijector = tfp.bijectors.ScaleMatvecLinearOperator(linop)

    q = tfd.MultivariateNormalLinearOperator(q_loc, q_scale_linop)
    q_new = tfd.TransformedDistribution(distribution=q, bijector=bijector)

    # np.testing.assert_allclose(loc_new, q_new.mean())
    # np.testing.assert_allclose(cov_new, q_new.covariance())
