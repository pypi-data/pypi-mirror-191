from gpflow.inducing_variables import InducingPoints


class InducingPointsExtended(InducingPoints):

    @classmethod
    def from_inducing_points(cls, inducing_points):
        return cls(inducing_points.Z, inducing_points.name)
