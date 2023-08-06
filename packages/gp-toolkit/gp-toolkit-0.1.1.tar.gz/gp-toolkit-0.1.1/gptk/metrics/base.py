import numpy as np
import tensorflow as tf


def mean_squared_error(y_test, y_pred, squared=False):
    # rmse = mean_squared_error(Y_test, f_loc_test.numpy(), 
    #                           multioutput="raw_values", squared=False)
    mse = tf.reduce_mean(tf.square(y_test - y_pred), axis=None)
    return mse if squared else tf.sqrt(mse)


def calculate_rmse(model, data, scale=None):
    X, Y = data
    f_loc, f_var = model.predict_f(X, full_cov=False)
    error = mean_squared_error(f_loc, Y, squared=False)

    if scale is not None:

        error *= scale

        # Below is equivalent to simply multiplying by `scale`:
        # error_ref = mean_squared_error(scale * f_loc, scale * Y, squared=False)
        # tf.debugging.assert_equal(error_ref, error)

    return error


def calculate_nlpd(model, data, scale=None):

    nlpd = tf.math.negative(model.predict_log_density(data))

    if scale is not None:

        nlpd += np.log(scale)

        # Below is equivalent to simply adding `np.log(scale)`:
        # X, Y = data
        # f_mean, f_var = model.predict_f(X)

        # # TODO(LT): Issue a warning that we are modifying the learned 
        # # hyperparameter here!
        # model.likelihood.variance *= scale**2
        # nlpd_ref = - model.likelihood.predict_log_density(f_mean * scale, 
        #                                                   f_var * scale**2,
        #                                                   Y * scale)
        # tf.debugging.assert_near(nlpd_ref, nlpd)

    return tf.reduce_mean(nlpd, axis=None)
