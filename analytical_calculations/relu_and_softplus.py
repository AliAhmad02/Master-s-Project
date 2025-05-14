from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from utilities import savefig

FNAME = Path(__file__).stem
plt.style.use("science")

plt.rc(
    "text.latex",
    preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{amsfonts}",
)

x = np.linspace(-2, 2, 1000)


def relu(x):
    return (x + np.abs(x)) / 2


def softplus(x):
    return np.logaddexp(0, x)


fig, ax = plt.subplots(1, 1, figsize=(2.2, 2.2))
ax.plot(x, relu(x), color="tab:orange", lw=1.5, label="ReLU")
ax.plot(x, softplus(x), color="black", lw=1.5, ls="dashed", label="Softplus")
ax.set_xlabel("Input", fontsize=10)
ax.set_ylabel("Output", fontsize=10)
ax.legend(frameon=False, fontsize=10)
savefig(FNAME, "softplus_relu", fig, svg=True)
plt.show()
