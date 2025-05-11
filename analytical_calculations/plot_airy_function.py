import matplotlib.pyplot as plt
from scipy import special
import numpy as np
import scienceplots
from utilities import savefig
from pathlib import Path

FNAME = Path(__file__).stem

plt.style.use("science")

plt.rc('text.latex', preamble=r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{amsfonts}')

# Here, k is the "kind" of the airy function
def airy(k: int, z: float) -> float:
    if not isinstance(k, int) or k not in [0, 1, 2, 3]:
        raise ValueError("k must be an integer between 0 and 3.")
    else:
        return special.airy(z)[k]

xi = np.linspace(-5, 10, 10_000)
y = airy(1, -xi) ** 2 + xi * airy(0, -xi) ** 2
fig, ax = plt.subplots(1, 1, figsize=(5, 4))
ax.plot(xi, y, color="k", lw=1.5)
ax.set_xlabel(r"$\xi$", fontsize=22)
ax.tick_params(axis='both', which='major', labelsize=13)
ax.tick_params(axis='both', which='minor', labelsize=13)
ax.set_ylabel(r"$\alpha_{FK} / (\alpha_b \sqrt{\beta} \pi)$", fontsize=22)
# savefig(FNAME, "airy_plot", fig, svg=True)
plt.show()