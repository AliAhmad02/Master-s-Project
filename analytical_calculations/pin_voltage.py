import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import scienceplots
from utilities import savefig
from pathlib import Path

plt.style.use("science")

plt.rc('text.latex', preamble=r'\usepackage{amsmath}\usepackage{amssymb}\usepackage{amsfonts}')

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

w_d_300K = d_p_300K + d_n_300K + 94

print((v_bi_300K + 6.5) / ((sum(depletion_width(d_i, v_bi_300K, -6.5))+ 94) * 1e-4))
# Field in kv/cm
field = (v_bi_300K - voltages) / (1e-4 * w_d_300K)

fig, ax = plt.subplots(1, 1, figsize=(2.4, 2.4))
ax.set_xlabel(r"Reverse bias voltage [$\mathrm{V}$]", fontsize=10)
ax.set_ylabel(r"Depletion width [$\mathrm{nm}$]", fontsize=10)
ax.plot(-voltages, d_n_300K, label=r"$d_n$", color="tab:blue", lw=1.5)
ax.plot(-voltages, d_p_300K, label=r"$d_p$", color="tab:red", lw=1.5)
# ax.plot(-voltages, w_d_300K, label=r"$w_d$", color="black")
# ax.plot(-voltages, depletion_widths_4K, label=r"$4K$", ls="dashed")
ax.axhline(n_w, ls="dashed", lw=1.5, color="tab:blue")
ax.axhline(p_w, ls="dashed", lw=1.5, color="tab:red")

trans = transforms.blended_transform_factory(
    ax.get_yticklabels()[0].get_transform(), ax.transData)
ax.text(0, p_w-0.3, rf"$w_p$", color="tab:red", transform=trans, ha="right", va="center", fontsize=10)

trans = transforms.blended_transform_factory(
    ax.get_yticklabels()[0].get_transform(), ax.transData)
ax.text(0, n_w+0.3, rf"$w_n$", color="tab:blue", transform=trans, ha="right", va="center", fontsize=10)
ax.get_yticklabels()[2].set_visible(False)
ax.legend(fontsize=10, frameon=False)
# savefig(FNAME, "dep_width_volts", fig, svg=True)
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(2.4, 2.4))
ax.set_xlabel(r"Reverse bias voltage [$\mathrm{V}$]", fontsize=10)
ax.set_ylabel(r"Field strength [$\mathrm{kV/cm}$]", fontsize=10)
ax.plot(-voltages[field<=500], field[field<=500], color="black", lw=1.5, label=r"$F(V_{{rev}})$")
ax.axvspan(*-voltages[(field>=400) & (field<=500)][[0, -1]], color="black", alpha=0.3, label="Breakdown")
ax.legend(frameon=False, fontsize=10, loc="upper left")
# savefig(FNAME, "field_volts", fig, svg=True)
plt.show()