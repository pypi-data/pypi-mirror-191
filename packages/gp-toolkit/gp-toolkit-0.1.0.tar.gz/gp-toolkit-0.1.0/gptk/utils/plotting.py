import numpy as np
import seaborn as sns


def setup_aesthetic(width, dpi, use_tex, context, style, palette, height=None, 
                    aspect=.5*(1+np.sqrt(5))):

    print("GOT HERE!!! GOT HERE!!! GOT HERE!!! GOT HERE!!! GOT HERE!!! GOT HERE!!! GOT HERE!!!")

    if height is None:
        height = aspect * width

    figsize = width, height

    rc = {
        "figure.figsize": figsize,
        "figure.dpi": dpi,
        "font.serif": ["Palatino", "Times", "Computer Modern"],
        "text.usetex": use_tex,
        "text.latex.preamble": r"\usepackage{nicefrac}",
    }
    sns.set(context=context, style=style, palette=palette, font="serif", rc=rc)
    return figsize
