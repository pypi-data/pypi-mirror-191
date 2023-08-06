import numpy as np
import pandas as pd

# from importlib.resources import files
from pathlib import Path
from sklearn.utils import Bunch


def load_snelson_1d():

    # path = files('gptk.datasets.data').joinpath('snelson1d.npz')
    path = Path(__file__).parent.joinpath('data', 'snelson1d.npz')

    with np.load(path) as dataset:
        data = dataset['X']
        target = dataset['Y']

    return Bunch(data=data, target=target)


def load_motorcycle():

    """
    Motorcycle dataset.

    Examples
    --------

    .. plot::
        :include-source:
        :context: close-figs

        from gptk.datasets import load_motorcycle

        motorcycle = load_motorcycle()

        fig, ax = plt.subplots()

        ax.scatter(motorcycle.data, motorcycle.target, s=3.0, marker='o', color='k', alpha=0.8)

        ax.set_xlabel("times")
        ax.set_ylabel("acceleration")

        plt.show()
    """

    path = Path(__file__).parent.joinpath('data', 'motor.csv')
    frame = pd.read_csv(path, index_col=0)

    return Bunch(
        data=frame[["times"]].to_numpy(),
        target=frame[["accel"]].to_numpy(),
    )
