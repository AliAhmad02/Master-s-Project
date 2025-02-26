import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import scienceplots
from utilities import savefig
from pathlib import Path

plt.style.use("science")

FNAME = Path(__file__).stem

p_w = 35 # Width of the p-layer
n_w = 38.5 # Width of the n-layer
d_i = 94 # intrinsic thickness in nm
v_bi_300K = 1.406 # Built in voltage at room temperature
v_bi_4K = 1.424 # Built in voltage at 4K

# We assume that N_D/N_A=2
def depletion_width(d_i, v_bi, v_app):
    d_n = (-2 * d_i + np.sqrt(4 * d_i ** 2 + 12 * 722.9 * (v_bi - v_app))) / 6
    d_p = 2 * d_n
    return d_p, d_n

voltages = np.linspace(0, -12, 1000)
d_p_300K, d_n_300K = depletion_width(d_i, v_bi_300K, voltages)
d_p_4K, d_n_4K = depletion_width(d_i, v_bi_4K, voltages)

fig, ax = plt.subplots(1, 1, figsize=(5, 4))
ax.set_xlabel(r"Reverse bias voltage [$V$]", fontsize=14)
ax.set_ylabel(r"Depletion width [$nm$]", fontsize=14)
ax.plot(-voltages, d_n_300K, label=r"$d_n$", color="tab:blue")
ax.plot(-voltages, d_p_300K, label=r"$d_p$", color="tab:red")
# ax.plot(-voltages, depletion_widths_4K, label=r"$4K$", ls="dashed")
ax.axhline(n_w, label="n-layer thickness", ls="dashed", lw=1.5, color="tab:blue")
ax.axhline(p_w, label="p-layer thickness", ls="dashed", lw=1.5, color="tab:red")
ax.legend(fontsize=14, frameon=False)
# savefig(FNAME, "dep_width_volts", fig)
plt.show()
