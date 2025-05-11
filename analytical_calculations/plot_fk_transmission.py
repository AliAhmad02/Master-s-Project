import pathlib
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from FK_fitmodel import FK_fit_power
from utilities import savefig

plt.style.use("science")

FNAME = Path(__file__).stem


def plot_transmission(xdata, ydatas, labels):
    fig, ax = plt.subplots(1, 1, figsize=(2.2, 2.2))
    ax.plot(xdata, ydatas[0], label=labels[0], lw=1.5, color="tab:blue")
    ax.plot(xdata, ydatas[1], label=labels[1], lw=1.5, color="tab:orange")
    ax.plot(xdata, ydatas[2], label=labels[2], lw=1.5, color="tab:red")

    ax.set_xlabel("Incident power [$\mu W$]", fontsize=10)
    ax.set_ylabel("Transmitted power [$\mu W$]", fontsize=10)
    ax.legend(frameon=False, fontsize=10)
    return fig, ax


p_in_vals = np.linspace(0, 100, 500)
wavelengths = np.linspace(900, 1000, 200)
# Power in muW, eta in unitless, R in Mohm, L in cm, lambda in nm, T in K, V_app in V
fk_transmission = lambda lam, voltage, L, R: FK_fit_power(
    p_in_vals, 1, R, L, lam, 0, 298, voltage, 0
)[0]

fk_absorption = lambda lam, voltage, L, R: FK_fit_power(
    p_in_vals, 1, R, L, lam, 0, 298, voltage, 0
)[1]

fk_transmissions_wavelengths = []

for wavelength in wavelengths:
    fk_transmissions_wavelengths.append(fk_transmission(wavelength, -4, 3.5e-3, 0.1))

fk_transmissions_wavelengths = np.array(fk_transmissions_wavelengths)

fk_absorption_900nm = fk_absorption(900, -4, 3.5e-3, 0.1)
fk_voltage_900nm = -4 + p_in_vals * 0.1 * (1 - np.exp(-3.5e-3 * (fk_absorption_900nm)))

fk_absorption_930nm = fk_absorption(930, -4, 3.5e-3, 0.1)
fk_voltage_930nm = -4 + p_in_vals * 0.1 * (1 - np.exp(-3.5e-3 * (fk_absorption_930nm)))

fk_absorption_980nm = fk_absorption(980, -4, 3.5e-3, 0.1)
fk_voltage_980nm = -4 + p_in_vals * 0.1 * (1 - np.exp(-3.5e-3 * (fk_absorption_980nm)))

trans_900nm = fk_transmission(900, -4, 3.5e-3, 0.1)
trans_930nm = fk_transmission(930, -4, 3.5e-3, 0.1)
trans_980nm = fk_transmission(980, -4, 3.5e-3, 0.1)

trans_10k = fk_transmission(930, -4, 3.5e-3, 0.01)
trans_100k = fk_transmission(930, -4, 3.5e-3, 0.1)
trans_1m = fk_transmission(930, -4, 3.5e-3, 1.0)

trans_m01V = fk_transmission(930, -0.1, 3.5e-3, 0.1)
trans_m2V = fk_transmission(930, -2, 3.5e-3, 0.1)
trans_m4V = fk_transmission(930, -4, 3.5e-3, 0.1)

trans_10mum = fk_transmission(930, -1, 1.0e-3, 0.1)
trans_100mum = fk_transmission(930, -1, 5.0e-3, 0.1)
trans_500mum = fk_transmission(930, -1, 30e-3, 0.1)

fig, ax = plot_transmission(
    p_in_vals,
    [trans_900nm, trans_930nm, trans_980nm],
    ["900 nm", "930 nm", "980 nm"],
)
# savefig(FNAME, "nl_trans_wls", fig, svg=True)
# plt.show()

fig, ax = plot_transmission(
    p_in_vals,
    [trans_m01V, trans_m2V, trans_m4V][::-1],
    ["-0.1V", "-2V", "-4V"][::-1],
)
# savefig(FNAME, "nl_trans_voltages", fig, svg=True)
# plt.show()

fig, ax = plot_transmission(
    p_in_vals,
    [trans_10mum, trans_100mum, trans_500mum][::-1],
    [r"10$\mu m$", "50$\mu m$", "300$\mu m$"][::-1],
)
# savefig(FNAME, "nl_trans_ls", fig, svg=True)
# plt.show()

fig, ax = plot_transmission(
    p_in_vals,
    [trans_10k, trans_100k, trans_1m],
    [
        r"10 $k\Omega$",
        r"100 $k\Omega$",
        r"1 $M\Omega$",
    ],
)
# savefig(FNAME, "nl_trans_resistances", fig, svg=True)
# plt.show()

fig = plt.figure(figsize=(2.2, 3.0))
plt.plot(p_in_vals, fk_voltage_900nm, lw=1.5, color="tab:blue", label=r"900 nm")
plt.plot(p_in_vals, fk_voltage_930nm, lw=1.5, color="tab:orange", label=r"930 nm")
plt.plot(p_in_vals, fk_voltage_980nm, lw=1.5, color="tab:red", label=r"980 nm")
plt.xlabel(r"Incident power [$\mu W$]", fontsize=10)
plt.ylabel("Voltage across device [V]", fontsize=10)
plt.legend(frameon=False, fontsize=10, handlelength=1.3)
savefig(FNAME, "nl_voltagedrop", fig, svg=True)
# plt.show()

fig = plt.figure(figsize=(2.2, 3.0))
plt.plot(
    wavelengths,
    fk_transmissions_wavelengths[:, 5] / p_in_vals[5] * 100,
    lw=1.5,
    color="tab:blue",
    label=f"{p_in_vals[5]:.0f} $\mu W$",
)

plt.plot(
    wavelengths,
    fk_transmissions_wavelengths[:, 50] / p_in_vals[50] * 100,
    lw=1.5,
    color="tab:orange",
    label=f"{p_in_vals[50]:.0f} $\mu W$",
)

plt.plot(
    wavelengths,
    fk_transmissions_wavelengths[:, 150] / p_in_vals[150] * 100,
    lw=1.5,
    color="tab:red",
    label=f"{p_in_vals[150]:.0f} $\mu W$",
)
plt.xlabel("Wavelength [nm]", fontsize=10)
plt.ylabel(r"Transmission (\%)", fontsize=10)
plt.legend(frameon=False, fontsize=10, handlelength=1.3)
savefig(FNAME, "nl_trans_wl_range", fig, svg=True)
# plt.show()
