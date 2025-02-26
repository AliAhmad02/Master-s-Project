import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")


def savefig(FNAME: str, fig_name: str, fig: Figure, tight=True):

    SAVEFIG_DIR = os.path.join(FIGDIR, FNAME)
    FIGPATH = os.path.join(SAVEFIG_DIR, f"{fig_name}.png")

    if not os.path.exists(SAVEFIG_DIR):
        os.mkdir(SAVEFIG_DIR)

    if tight:
        fig.savefig(FIGPATH, dpi=300, bbox_inches="tight")
    else:
        fig.savefig(FIGPATH, dpi=300)
