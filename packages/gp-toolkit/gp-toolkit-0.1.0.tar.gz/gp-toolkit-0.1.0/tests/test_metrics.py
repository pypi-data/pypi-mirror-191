import pytest

import tensorflow as tf
import numpy as np

from gptk.datasets import load_snelson_1d
from gptk.metrics import calculate_rmse, calculate_nlpd, mean_squared_error

from gpflow.models import GPR

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def test_rmse(kernel, random_state):

    snelson_1d = load_snelson_1d()

    X_train, X_test, Y_train, Y_test = train_test_split(
        snelson_1d.data,
        snelson_1d.target,
        test_size=0.25,
        shuffle=True,
        random_state=random_state
    )

    feature_scaler = MinMaxScaler(feature_range=(-1, 1))
    target_scaler = StandardScaler()

    X_train = feature_scaler.fit_transform(X_train)
    X_test = feature_scaler.transform(X_test)

    Y_train_std = target_scaler.fit_transform(Y_train)
    Y_test_std = target_scaler.transform(Y_test)

    train_data = X_train, Y_train_std
    test_data = X_test, Y_test_std

    loc = target_scaler.mean_.item()
    scale = target_scaler.scale_.item()

    model = GPR(train_data, kernel=kernel)
    f_loc_std, f_var_std = model.predict_f(X_test, full_cov=False)

    # sqrt{sum_i ((yi - fi)**2)}
    # = sqrt{sum_i ((yi - m - fi + m)**2)}
    # = sqrt{sum_i (((yi - m) - (fi - m))**2)}
    # = sqrt{s**2 sum_i ((yi - m)/s - (fi - m)/s)**2}
    # = s * sqrt{sum_i ((yi - m)/s - (fi - m)/s)**2}

    rmse = calculate_rmse(model, test_data, scale)
    rmse1 = scale * mean_squared_error(Y_test_std, f_loc_std)
    rmse2 = mean_squared_error(Y_test, f_loc_std * scale + loc)

    np.testing.assert_allclose(rmse, rmse1)
    np.testing.assert_allclose(rmse1, rmse2)

    nlpd = calculate_nlpd(model, test_data, scale)

    nlpds1 = np.log(scale) - model.predict_log_density(test_data)
    nlpd1 = tf.reduce_mean(nlpds1, axis=None)

    np.testing.assert_allclose(nlpd, nlpd1)

    model.likelihood.variance *= scale**2
    nlpds2 = - model.likelihood.predict_log_density(
        f_loc_std * scale + loc,
        f_var_std * scale**2,
        Y_test
    )

    np.testing.assert_allclose(nlpds1, nlpds2)


def test_scale(random_state):

    snelson_1d = load_snelson_1d()

    X_train, X_test, Y_train, Y_test = train_test_split(
        snelson_1d.data,
        snelson_1d.target,
        test_size=0.25,
        shuffle=True,
        random_state=random_state
    )

    target_scaler = StandardScaler().fit(Y_train)

    Y_test_std = target_scaler.transform(Y_test)
    Y_pred_std = Y_test_std + random_state.randn(*Y_test_std.shape)

    error1 = target_scaler.scale_ * mean_squared_error(Y_test_std, Y_pred_std, squared=False)
    error2 = mean_squared_error(
        target_scaler.inverse_transform(Y_test_std),
        target_scaler.inverse_transform(Y_pred_std), 
        squared=False
    )

    np.testing.assert_array_equal(error1, error2)
