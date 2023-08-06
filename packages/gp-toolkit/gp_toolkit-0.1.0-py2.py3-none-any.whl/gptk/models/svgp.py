from gpflow.models.svgp import SVGP_deprecated as SVGPBase

from .utils import create_variational_loc, create_variational_scale


class SVGP(SVGPBase):

    def __init__(
        self,
        kernel,
        likelihood,
        inducing_variable,
        q_loc,
        q_scale_linop,
        q_white: bool = False,
        mean_fn=None,
        output_dim: int = 1,
        n_train=None,
    ):
        # Beware: This calls the initializer of SVGPBase's parent and
        #   completely bypasses SVGPBase's own initializer.
        super(SVGPBase, self).__init__(kernel, likelihood, mean_fn, output_dim)

        # self.inducing_variable = inducingpoint_wrapper(inducing_variable)
        self.inducing_variable = inducing_variable

        self.q_loc = q_loc
        self.q_scale_linop = q_scale_linop

        self.q_white = q_white
        self.n_train = n_train

    @classmethod
    def from_default(cls, kernel, likelihood, inducing_variable,
                     q_loc_initializer="zeros",
                     q_scale_initializer=None,
                     q_white: bool = False, q_diag: bool = False,
                     mean_fn=None, output_dim: int = 1, n_train=None):

        n_inducing = inducing_variable.num_inducing

        q_loc = create_variational_loc(output_dim, n_inducing,
                                       q_loc_initializer)
        q_scale_linop = create_variational_scale(output_dim, n_inducing,
                                                 q_diag, q_scale_initializer)

        return cls(kernel, likelihood, inducing_variable,
                   q_loc, q_scale_linop, q_white,
                   mean_fn, output_dim, n_train)

    @property
    def n_inducing(self):
        """
        Alias.
        """
        return self.inducing_variable.num_inducing

    @property
    def output_dim(self):
        """
        Alias.
        """
        return self.num_latent_gps

    @property
    def mean_fn(self):
        """
        Alias.
        """
        return self.mean_function

    @property
    def q_mu(self):
        """
        Alias.
        """
        return self.q_loc

    @property
    def q_sqrt(self):
        """
        Alias.
        """
        return self.q_scale_linop

    @property
    def num_data(self):
        """
        Alias.
        """
        return self.n_train

    @property
    def whiten(self):
        """
        Alias.
        """
        return self.q_white
