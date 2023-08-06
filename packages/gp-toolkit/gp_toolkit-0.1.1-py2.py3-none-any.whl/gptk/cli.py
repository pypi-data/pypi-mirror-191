"""Console script for gptk."""
import sys
import click
import logging

import numpy as np

from rich.logging import RichHandler

from gpflow.models.svgp import SVGP_deprecated as SVGP
from gpflow.likelihoods import Gaussian
from gpflow.kernels import SquaredExponential, Matern52
from gpflow.inducing_variables import InducingPoints

import gptk


@click.command()
def main(args=None):
    """Console script for gptk."""
    logging.basicConfig(
        level="DEBUG", format="%(message)s", datefmt="[%X]",
        handlers=[RichHandler(markup=True, rich_tracebacks=True,
                              tracebacks_suppress=[click])]
    )
    logger = logging.getLogger(__name__)
    logger.info("Replace this message by putting your code into "
                "gptk.cli.main")
    logger.info("See click documentation at https://click.palletsprojects.com/")

    # lengthscales = np.full((input_dim,), fill_value=lengthscale) if ard else lengthscale
    # override()

    full_cov = False
    full_output_cov = False

    seed = 8888

    n_test = 128
    n_inducing = 32

    input_dim = 5

    noise_scale = 0.5
    noise_variance = noise_scale**2

    whiten = False

    random_state = np.random.RandomState(seed)

    X_test = random_state.randn(n_test, input_dim)

    kernel = SquaredExponential()
    likelihood = Gaussian(variance=noise_variance)
    inducing_variable = InducingPoints(Z=random_state.randn(n_inducing, input_dim))

    model = SVGP(
        kernel=kernel,
        likelihood=likelihood,
        inducing_variable=inducing_variable,
        mean_function=None, 
        whiten=whiten,
    )
    mu, cov = model.predict_f(X_test, full_cov=full_cov, full_output_cov=full_output_cov)

    logger.info(mu.shape)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
