import pytest

import numpy as np

from tensorflow.keras.initializers import RandomNormal, TruncatedNormal

from gpflow.kernels import Matern52
from gpflow.inducing_variables import InducingPoints
from gpflow.covariances import Kuu, Kuf
from gpflow.config import default_jitter

from gptk.models.utils import (
    create_variational_loc, 
    create_variational_scale
)


@pytest.fixture(params=[Matern52, ])
def kernel(request):
    return request.param()


@pytest.fixture(params=range(5))
def seed(request):
    return request.param


@pytest.fixture(params=[1, 5])
def input_dim(request):
    return request.param


@pytest.fixture(params=[1, 3])
def output_dim(request):
    return request.param


# @pytest.fixture(params=[32,])
@pytest.fixture(params=[1, 32])
def n_inducing(request):
    return request.param


@pytest.fixture(params=[128, ])
def n_test(request):
    return request.param


@pytest.fixture(params=[False, True])
def q_diag(request):
    return request.param


@pytest.fixture
def random_state(seed):
    return np.random.RandomState(seed)


@pytest.fixture
def X_test(n_test, input_dim, random_state):
    return random_state.randn(n_test, input_dim)


@pytest.fixture
def inducing_variable(n_inducing, input_dim, random_state):
    return InducingPoints(random_state.randn(n_inducing, input_dim))  # [M, D]


@pytest.fixture
def Kmm(inducing_variable, kernel):    
    return Kuu(inducing_variable, kernel, jitter=default_jitter())  # [M, M]


@pytest.fixture
def Kmn(inducing_variable, kernel, X_test):
    return Kuf(inducing_variable, kernel, X_test)  # [M, N]


@pytest.fixture
def q_loc(output_dim, n_inducing, seed):
    q_loc_initializer = RandomNormal(stddev=1., seed=seed)
    return create_variational_loc(output_dim, n_inducing, q_loc_initializer)


@pytest.fixture
def q_scale_linop(output_dim, n_inducing, q_diag, seed):
    q_scale_initializer = TruncatedNormal(mean=1., seed=seed) if q_diag \
         else RandomNormal(seed=seed)
    return create_variational_scale(output_dim, n_inducing, q_diag,
                                    q_scale_initializer)
