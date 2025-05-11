import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
from scipy.interpolate import make_smoothing_spline
import scienceplots
from utilities import savefig

FNAME = Path(__file__).stem

plt.style.use("science")

fig = plt.figure(figsize=(3, 5))

parent_dir = Path(__file__).parent
data = np.loadtxt(os.path.join(parent_dir, "data", "GaAs_bands_soc.dat.gnu"))

k = np.unique(data[:, 0])
bands = np.reshape(data[:, 1], (-1, len(k)))

kmin, kmax = 0, 1.3
Emin, Emax = 3, 15
k_linspace = np.linspace(kmin, kmax, 5000)

ticks = [kmin, (0.61 + kmin) / 2, 0.61, (0.61 + kmax) / 2, kmax]

L, lam, gamma, delta, X = ticks

for band in range(12, 25):
    if band > 17:
        bands[band, :] += 1.4
    spl = make_smoothing_spline(k, bands[band, :])
    plt.plot(k_linspace, spl(k_linspace), linewidth=1.3, color="k")

plt.xlim(kmin, kmax)
plt.ylim(Emin, Emax)

conduction_band_min = 7.8859139245206835
valence_band_max = 6.368046260362119
annotation_pos = 0.8

plt.xlabel("Wavevector", fontsize=14)
plt.xticks(
    ticks=ticks, labels=["L", "$\Lambda$", "$\Gamma$", "$\Delta$", "X"], fontsize=15
)
plt.axhline(
    valence_band_max,
    lw=1,
    ls="dashed",
    color="k",
    xmin=0.61 / kmax,
    xmax=annotation_pos / kmax,
)
plt.axhline(
    conduction_band_min,
    ls="dashed",
    color="k",
    xmin=0.61 / kmax,
    xmax=annotation_pos / kmax,
)
plt.annotate(
    "",
    xy=(annotation_pos, conduction_band_min),
    xycoords="data",
    xytext=(annotation_pos, valence_band_max),
    textcoords="data",
    arrowprops={"arrowstyle": "<->"},
)
plt.annotate(
    "$E_g$=1.42 eV",
    xy=(annotation_pos, np.mean([valence_band_max, conduction_band_min])),
    xycoords="data",
    xytext=(2.2, 0),
    textcoords="offset points",
    fontsize=12,
    va="center",
)
plt.text(0.05, 5.6, "HH", fontsize=12)
plt.text(0.05, 4.5, "LH", fontsize=12)
plt.text(0.33, 4.5, "SO", fontsize=12)
plt.text(0.05, 7.8, "CB", fontsize=12)
plt.tick_params(labelleft=False)
# savefig(FNAME, "gaas_bands", fig, svg=True)
plt.show()
