import numpy as np
import matplotlib.pyplot as plt
from utilities import savefig
import scienceplots
from pathlib import Path

FNAME = Path(__file__).stem

plt.style.use("science")

a = 1
k_lin = np.linspace(-np.pi / a, np.pi / a, 1000)
E_gap = 1.5
E0_0 = -1 * E_gap / 2
E1_0 = 1 * E_gap / 2

B0 = 0.1
B1 = -0.1

E0 = E0_0 + 2 * B0 * np.cos(k_lin * a)
E1 = E1_0 + 2 * B1 * np.cos(k_lin * a)

fig = plt.figure(figsize=(3, 5))
plt.plot(k_lin, E0, color="k", lw=1.3)
plt.plot(k_lin, E1, color="k", lw=1.3)
plt.scatter(k_lin[::110][1:-1], E0[::110][1:-1], color="k")
plt.scatter(k_lin[::110][1:-1], E1[::110][1:-1], color="white", edgecolors="black")

plt.annotate(
    "",
    xy=(0, E1.min()),
    xycoords="data",
    xytext=(0, E0.max()),
    textcoords="data",
    arrowprops={"arrowstyle": "<->"},
)

plt.text(0, 0, r"$E_g$", fontsize=12, va="center", ha="center", bbox=dict(facecolor="white", edgecolor="white"))

min_val = np.concatenate((E0, E1)).min()
max_val = np.concatenate((E0, E1)).max()

plt.xticks([-np.pi/a, 0, np.pi/a], ["$-\pi/a$", "0", "$+\pi/a$"], fontsize=15)
plt.xlim([-np.pi/a, np.pi/a])
plt.tick_params(labelleft = False)
plt.xlabel("Wavevector", fontsize=14)
plt.text(0, -0.7, "p-type", ha="center", va="center", fontsize=12)
plt.text(0, 0.7, "s-type", ha="center", va="center", fontsize=12)
# savefig(FNAME, "tightbinding_bands", fig, svg=True)
plt.show()