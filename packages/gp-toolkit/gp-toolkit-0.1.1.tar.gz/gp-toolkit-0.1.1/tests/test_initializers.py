#!/usr/bin/env python

"""Tests for `gptk` package."""
import pytest

import numpy as np
import tensorflow as tf

from gptk.initializers import Identity
from gpflow.config import default_float


@pytest.mark.parametrize("shape", [(3, 3), (3, 4), (2, 3, 4), (8, 2, 3, 4)])
def test_identity_initializer(shape):

    initializer = Identity()
    initial_value = initializer(shape, dtype=default_float())

    assert initial_value.shape == shape

    *batch_shape, num_rows, num_columns = shape
    eyes = tf.eye(num_rows, num_columns, batch_shape, dtype=default_float())

    np.testing.assert_array_equal(initial_value, eyes)


def test_identity_initializer_exception():
    with pytest.raises(ValueError):
        initializer = Identity()
        initializer(shape=(5,), dtype=default_float())
