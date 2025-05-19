from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from FK_fitmodel import FK_fit
from utilities import savefig

FNAME = Path(__file__).stem

plt.style.use("science")


plt.rc(
    "text.latex",
    preamble=r"\usepackage{amsmath}\usepackage{amssymb}\usepackage{amsfonts}",
)

voltages = np.linspace(0, -4, 10_000)
wavelengths = np.linspace(920, 980, 10_000)

fk_fit_wavelengths_4V = FK_fit(wavelengths, 0, 298, -4)
fk_fit_wavelengths_2V = FK_fit(wavelengths, 0, 298, -2)
fk_fit_wavelengths_1V = FK_fit(wavelengths, 0, 298, -1)

fk_fit_voltages_920 = FK_fit(920, 0, 298, voltages)
fk_fit_voltages_935 = FK_fit(935, 0, 298, voltages)
fk_fit_voltages_950 = FK_fit(950, 0, 298, voltages)

fig, ax = plt.subplots(1, 1, figsize=(2.2, 2.2))
ax.plot(
    -voltages, fk_fit_voltages_920, label=r"920 $\mathrm{nm}$", color="tab:blue", lw=1.5
)
ax.plot(
    -voltages,
    fk_fit_voltages_935,
    label=r"935 $\mathrm{nm}$",
    color="tab:orange",
    lw=1.5,
)
ax.plot(
    -voltages, fk_fit_voltages_950, label=r"950 $\mathrm{nm}$", color="tab:red", lw=1.5
)

ax.set_xlabel(r"Reverse voltage [$\mathrm{V}$]", fontsize=10)
ax.set_ylabel(r"$\alpha_{FK} \ [\mathrm{cm^{-1}}]$", fontsize=10)
ax.legend(frameon=False, fontsize=10)

savefig(FNAME, "fk_absorption_voltages", fig, svg=True)


fig, ax = plt.subplots(1, 1, figsize=(2.2, 2.2))
ax.plot(
    wavelengths,
    fk_fit_wavelengths_1V,
    label=r"-1$\mathrm{V}$",
    color="tab:blue",
    lw=1.5,
)
ax.plot(
    wavelengths,
    fk_fit_wavelengths_2V,
    label=r"-2$\mathrm{V}$",
    color="tab:orange",
    lw=1.5,
)

ax.plot(
    wavelengths,
    fk_fit_wavelengths_4V,
    label=r"-4$\mathrm{V}$",
    color="tab:red",
    lw=1.5,
)

ax.set_xlabel(r"Wavelength [$\mathrm{nm}$]", fontsize=10)
ax.set_ylabel(r"$\alpha_{FK} \ [\mathrm{cm^{-1}}]$", fontsize=10)
ax.legend(frameon=False, fontsize=10)

savefig(FNAME, "fk_absorption_wavelengths", fig, svg=True)
