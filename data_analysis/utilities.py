from matplotlib.figure import Figure
import os
import numpy as np
from scipy import special
from scipy.optimize import fsolve
from dataclasses import dataclass
from typing import Callable
import inspect
from iminuit import Minuit
from iminuit.cost import LeastSquares, BinnedNLL, UnbinnedNLL
from scipy.stats import chi2

FIGDIR = os.path.join(os.path.dirname(__file__), "figures")


def num_err_to_latex_str(number: float, err: float) -> str:
    """Take a large/small number (including its error) that should be written
    in scientific notation and format it as a latex-string.

    For example, 3.55e+7±0.05e+7 will be written as $(3.55±0.05)\times 10^{7}$.

    We do not use powers of 10 if abs(power) is 2 and below.

    Args:
        number: Number to be formatted.
        err: The error on the number.
        n_decimals: Number of decimals to format the number/error with.

    Return:
        latex_string: The formatted latex-string.
    """
    power_of_ten: int = int(np.floor(np.log10(np.abs(number))))

    if abs(power_of_ten) <= 2:
        n_decimals = int(-np.floor(np.log10(np.abs(err))))
        latex_string: str = rf"${number:.{n_decimals}f} \pm {err:.{n_decimals}f}$"
    else:
        num_no_power: float = number / (10**power_of_ten)
        err_no_power: float = err / (10**power_of_ten)
        n_decimals = int(-np.floor(np.log10(np.abs(err_no_power))))
        if n_decimals < 0:
            n_decimals = 0
        latex_string: str = (
            rf"$({num_no_power:.{n_decimals}f} \pm {err_no_power:.{n_decimals}f})\times 10^{{{power_of_ten}}}$"
        )
    return latex_string


def savefig(nb_name: str, fig_name: str, fig: Figure, tight=True, svg=False):

    SAVEFIG_DIR = os.path.join(FIGDIR, nb_name)

    if svg:
        FIGPATH = os.path.join(SAVEFIG_DIR, f"{fig_name}.svg")
    else:
        FIGPATH = os.path.join(SAVEFIG_DIR, f"{fig_name}.png")

    if not os.path.exists(SAVEFIG_DIR):
        os.mkdir(SAVEFIG_DIR)

    if tight:
        fig.savefig(FIGPATH, dpi=300, bbox_inches="tight")
    else:
        fig.savefig(FIGPATH, dpi=300)


def gaas_index(lam: float, x: float, T: float) -> float:
    lam = lam / 1000

    E = 1.0 / lam

    # Gehrsitz et al., Eq. (11) and below Eq. (11):
    E_Gamma_0 = 1.5192 / 1.239856  # OK
    E_Deb = 15.9e-3 / 1.239856  # OK
    E_TO = 33.6e-3 / 1.239856  # OK
    S = 1.8  # OK
    S_TO = 1.1  # OK
    kB = 0.0861708e-3 / 1.239856  # OK
    E_Gamma_GaAs = (
        E_Gamma_0
        + S * E_Deb * (1 - 1 / np.tanh(E_Deb / (2 * kB * T)))
        + S_TO * E_TO * (1 - 1 / np.tanh(E_TO / (2 * kB * T)))
    )  # OK, but cot rather than coth in original code!!!!!!!!

    # Gehrsitz et al., Table II, GaAs Fit 2 (Have not tried with Fit1...):
    a0 = 5.9613  # OK
    a1 = 7.178 * 1e-4  # OK
    a2 = -0.953 * 1e-6  # OK
    e0 = 4.7171  # OK
    e1 = -3.237 * 1e-4  # OK
    e2 = -1.358 * 1e-6  # OK

    # Gehrsitz et al., Page 7830, column 1:
    A0 = a0 + a1 * T + a2 * T**2  # OK
    E120 = e0 + e1 * T + e2 * T**2  # OK

    # Gehrsitz et al., Table IV:
    A = (
        A0 - 16.159 * x + 43.511 * x**2 - 71.317 * x**3 + 57.535 * x**4 - 17.451 * x**5
    )  # OK
    C1 = 21.5647 + 113.74 * x - 122.5 * x**2 + 108.401 * x**3 - 47.318 * x**4  # OK
    E12 = E120 + 11.006 * x - 3.08 * x**2  # OK
    invC0 = (
        50.535 - 150.7 * x - 62.209 * x**2 + 797.16 * x**3 - 1125 * x**4 + 503.79 * x**5
    )  # OK but sign ERROR in original code
    E0 = E_Gamma_GaAs + 1.1308 * x + 0.1436 * x**2  # OK
    # E0 = E_Gamma_GaAs + 1.136*x + 0.22*x**2#Also OK? Eq. (14).
    C0 = 1 / invC0

    C2_GaAs = 1.55 * 1e-3  # OK
    C2_AlAs = 2.61 * 1e-3  # OK
    E22_GaAs = 0.724 * 1e-3  # OK
    E22_AlAs = 1.331 * 1e-3  # OK
    E22 = E22_GaAs  # OK
    C2 = C2_GaAs  # OK

    E32 = E22_AlAs  # OK
    C3 = C2_AlAs  # OK
    R = (1 - x) * C2 / (E22 - E**2) + x * C3 / (E32 - E**2)  # OK
    eps = A + C0 / (E0**2 - E**2) + C1 / (E12 - E**2) + R  # OK
    n = np.sqrt(eps)  # OK
    return n


# Here, k is the "kind" of the airy function
def airy(k: int, z: float) -> float:
    if not isinstance(k, int) or k not in [0, 1, 2, 3]:
        raise ValueError("k must be an integer between 0 and 3.")
    else:
        return special.airy(z)[k]


def FK_absorption(lam: float, x: float, T: float, F: float) -> float:
    n = gaas_index(lam, x, T)  # GaAs refractive index (constant)
    mh1 = 0.087  # Light-hole effective mass
    mh2 = 0.45  # Heavy-hole effective mass
    mu1 = 0.0377
    mu2 = 0.0579
    fkcoeff = 0.58  # Experimental coefficient

    Eg = 1.519 - 5.405e-4 * T**2 / (T + 204)  # Temperature-dependent gap
    Eph = 1239.84 / lam

    beta1 = 1.1e5 * (Eg - Eph) * (2 * mu1) ** (1 / 3) * F ** (-2 / 3)
    beta2 = 1.1e5 * (Eg - Eph) * (2 * mu2) ** (1 / 3) * F ** (-2 / 3)

    a1 = (
        (1 + 1 / mh1)
        * (2 * mu1) ** (4 / 3)
        * (np.abs(airy(1, beta1)) ** 2 - beta1 * np.abs(airy(0, beta1)) ** 2)
    )
    a2 = (
        (1 + 1 / mh2)
        * (2 * mu2) ** (4 / 3)
        * (np.abs(airy(1, beta2)) ** 2 - beta2 * np.abs(airy(0, beta2)) ** 2)
    )

    FKa = (a1 + a2) * F ** (1 / 3) * 1e4 / n
    alpha = fkcoeff * FKa
    return alpha


def FK_fit(lam: float, x: float, T: float, V_d: float) -> float:
    # We do things in nanometers first then convert to centimeters
    # to avoid floating point issues. 795.5 is in units nm²/V
    depletion_width = 1e-7 * np.sqrt(1e4 + 795.5 * (1.4 - V_d))
    return FK_absorption(lam, x, T, -(V_d - 1.4) / depletion_width)


class FKFit:
    def __init__(
        self,
        P_in: float,
        R: float,
        L: float,
        lam: float,
        x: float,
        T: float,
        V_app: float,
    ) -> None:
        self.P_in = P_in
        self.R = R
        self.L = L
        self.lam = lam
        self.x = x
        self.T = T
        self.V_app = V_app
        self.alphas = []

    def FK_fit_power_unscaled(
        self,
        power: float,
        lam: float,
        V_app: float,
        R: float,
        eta: float,
        gamma: float,
        alpha_0: float,
    ) -> float:
        # func = (
        #     lambda alpha: FK_fit(
        #         lam,
        #         self.x,
        #         self.T,
        #         V_app + power * eta * R * (1 - np.exp(-alpha * self.L)),
        #     )
        #     + alpha_0
        #     - alpha
        # )

        func = (
            lambda alpha: FK_fit(
                lam,
                self.x,
                self.T,
                # Responsivity = eta * lam(mu m) / 1.24
                V_app
                + power * eta / 1.24 * (lam / 1000) * R
                * (1 - np.exp(-(gamma * alpha + alpha_0) * self.L)),
            )
            - alpha
        )
        if len(self.alphas) == 0:
            alpha = fsolve(func, 1000)[0]
        else:
            alpha = fsolve(func, self.alphas[-1])[0]
        self.alphas.append(alpha)
        P_out = power * np.exp(-self.L * (gamma * alpha + alpha_0))
        return float(P_out)

    def FK_fit_current(
        self,
        power: float,
        lam: float,
        V_app: float,
        R: float,
        eta: float,
        gamma: float,
        alpha_0: float,
    ) -> float:
        # func = (
        #     lambda alpha: FK_fit(
        #         lam,
        #         self.x,
        #         self.T,
        #         V_app + power * eta * R * (1 - np.exp(-alpha * self.L)),
        #     )
        #     + alpha_0
        #     - alpha
        # )
        # L_n = #2.5e-4 #0.01477
        func = (
            lambda alpha: FK_fit(
                lam,
                self.x,
                self.T,
                # Responsivity = eta * lam(mu m) / 1.24
                V_app
                + power * eta / 1.24 * (lam / 1000) * R * (1 - np.exp(-self.L * (gamma * alpha + alpha_0))),
                # + power * eta / 1.24 * (lam / 1000) * R * (1 - np.exp(-self.L * (gamma * alpha + alpha_0)) / (1 + L_n * (gamma * alpha + alpha_0))),
            )
            - alpha
        )
        if len(self.alphas) == 0:
            alpha = fsolve(func, 1000)[0]
        else:
            alpha = fsolve(func, self.alphas[-1])[0]
        self.alphas.append(alpha)
        current = (
            power
            * eta
            / 1.24
            * (lam / 1000)
            * (1 - np.exp(-self.L * (gamma * alpha + alpha_0)))
            # * (1 - np.exp(-self.L * (gamma * alpha + alpha_0)) / (1 + L_n * (gamma * alpha + alpha_0)))
        )
        return float(current)

    def FK_fit_current_array(
        self, power: np.ndarray, eta: float, gamma: float, alpha_0: float
    ) -> float:
        current = np.array(
            [
                self.FK_fit_current(
                    pow1, self.lam, self.V_app, self.R, eta, gamma, alpha_0
                )
                for pow1 in power
            ]
        )
        return current

    # def FK_fit_power_unscaled(
    #     self,
    #     power: float,
    #     lam: float,
    #     V_app: float,
    #     R: float,
    #     T_G: float,
    #     alpha_0: float,
    # ) -> float:
    #     eta = T_G * (1 - np.exp(-alpha * self.L))
    #     tau = 1e-6
    #     mu_n = 8500
    #     l = 1e-7 * np.sqrt(1e4 + 795.5 * (1.4 - V_d)) # depletion width in cm
    #     # res = mu_n * V_app * tau / l**2 * eta * (lam / 1000) / 1.24
    #     res = eta * V_app * lam * 68548.4
    #     func = (
    #         lambda alpha: FK_fit(
    #             lam,
    #             self.x,
    #             self.T,
    #             V_app + power * R * res,
    #         )
    #         + alpha_0
    #         - alpha
    #     )
    #     if len(self.alphas) == 0:
    #         alpha = fsolve(func, 1000)[0]
    #     else:
    #         alpha = fsolve(func, self.alphas[-1])[0]
    #     self.alphas.append(alpha)
    #     P_out = power * np.exp(-self.L * alpha)
    #     return float(P_out)

    def FK_fit_power_scaled(
        self, power: np.ndarray, eta: float, norm: float
    ) -> np.ndarray:
        P_out = np.array(
            [
                self.FK_fit_power_unscaled(pow1, self.lam, self.V_app, self.R, eta, 0.44, 23.5)
                for pow1 in power
            ]
        )
        return norm * P_out

    def FK_fit_voltage_scaled(
        self, voltage: np.ndarray, eta: float, alpha_0: float
    ) -> float:
        P_out = np.array(
            [
                self.FK_fit_power_unscaled(
                    self.P_in, self.lam, vol, self.R, eta, alpha_0
                )
                for vol in voltage
            ]
        )
        return P_out / np.max(P_out)

    def FK_fit_wavelength_scaled(
        self, wavelength: np.ndarray, eta: float, norm: float
    ) -> float:
        P_out = np.array(
            [
                self.FK_fit_power_unscaled(
                    self.P_in, wl, self.V_app, self.R, eta, 0.44, 23.5
                )
                for wl in wavelength
            ]
        )
        return norm * P_out


@dataclass
class FitInput:
    xdata: np.ndarray
    ydata: np.ndarray
    yerror: np.ndarray | None
    fit_func: Callable
    initial_guesses: list[float]


@dataclass
class FitResult:
    parameters: list[float]
    parameter_errors: list[float]
    chi2: float | None
    ndof: float | None
    p_value: float | None
    success: bool


def perform_fit(
    fit_input: FitInput,
    bounds: None | dict[str, tuple[float, float] | None] = None,
    outlier: int | list[int] | None = None,
    softloss=False,
):
    if (
        len(fit_input.initial_guesses)
        != len(inspect.signature(fit_input.fit_func).parameters) - 1
    ):
        raise ValueError("Initial guesses must match # of fit function arguments.")
    if outlier:
        xdata = np.delete(fit_input.xdata, outlier)
        ydata = np.delete(fit_input.ydata, outlier)
        yerror = np.delete(fit_input.yerror, outlier)
    else:
        xdata = fit_input.xdata
        ydata = fit_input.ydata
        yerror = fit_input.yerror

    if softloss:
        lstsq = LeastSquares(xdata, ydata, yerror, fit_input.fit_func, loss="soft_l1")
    else:
        lstsq = LeastSquares(xdata, ydata, yerror, fit_input.fit_func)
    minuit_obj = Minuit(lstsq, *fit_input.initial_guesses)

    if bounds:
        for name, bound in bounds.items():
            minuit_obj.limits[name] = bound

    minuit_obj.migrad()
    minuit_obj.hesse()

    chi2_val = minuit_obj.fval
    ndof = len(ydata) - minuit_obj.nfit
    p_val = chi2.sf(chi2_val, ndof)
    success = minuit_obj.accurate and minuit_obj.valid

    parameter_values = minuit_obj.values[:]
    parameter_errors = minuit_obj.errors[:]

    return FitResult(parameter_values, parameter_errors, chi2_val, ndof, p_val, success)


# def perform_fit_llh(
#     fit_input: FitInput,
#     bounds: None | dict[str, tuple[float, float] | None] = None,
#     outlier: int | list[int] | None = None,
# ):
#     if (
#         len(fit_input.initial_guesses)
#         != len(inspect.signature(fit_input.fit_func).parameters) - 1
#     ):
#         raise ValueError("Initial guesses must match # of fit function arguments.")
#     if outlier:
#         xdata = np.delete(fit_input.xdata, outlier)
#         ydata = np.delete(fit_input.ydata, outlier)
#         yerror = np.delete(fit_input.yerror, outlier)
#     else:
#         xdata = fit_input.xdata
#         ydata = fit_input.ydata
#         yerror = fit_input.yerror

#     counts, bin_edges = [[xdata[idx]] * ]

#     # binwidth = np.diff(xdata)[0]
#     # bin_edges = np.array([n * binwidth for n in range(len(xdata ) + 1)])
#     # bin_edges = (fit_input.xdata[:-1] + fit_input.xdata[1:])
#     # bin_edges = np.append(bin_edges, bin_edges[-1] + np.mean(np.diff(bin_edges)))
#     # bin_edges = np.append([0], bin_edges)
#     # if softloss:
#     #     lstsq = LeastSquares(xdata, ydata, yerror, fit_input.fit_func, loss="soft_l1")
#     # else:
#     #     lstsq = LeastSquares(xdata, ydata, yerror, fit_input.fit_func)
#     llh = BinnedNLL(ydata, bin_edges, fit_input.fit_func, use_pdf="approximate")
#     minuit_obj = Minuit(llh, *fit_input.initial_guesses)

#     if bounds:
#         for name, bound in bounds.items():
#             minuit_obj.limits[name] = bound

#     minuit_obj.migrad()
#     minuit_obj.hesse()

#     success = minuit_obj.accurate and minuit_obj.valid

#     parameter_values = minuit_obj.values[:]
#     parameter_errors = minuit_obj.errors[:]

#     return FitResult(parameter_values, parameter_errors, None, None, None, success)


def perform_fit_rounds(
    fit_input: FitInput,
    bounds: None | dict[str, float | None] = None,
    outlier: int | list[int] | None = None,
    opt_rounds: int = 10,
    softloss=False,
) -> FitResult:
    opt_round = 0
    success = False

    while (opt_round < opt_rounds) and not (success):
        intermediate_result = perform_fit(fit_input, bounds, outlier, softloss)

        par = intermediate_result.parameters
        fit_input.initial_guesses = par

        success = intermediate_result.success
        opt_round += 1

    fit_result = perform_fit(fit_input, bounds, outlier, softloss)
    return fit_result


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    p_in_vals = np.linspace(0, 100, 500)
    fk_fit = FKFit(p_in_vals, 1, 3.5e-3, 930, 0.3, 298, -4)
    sol = fk_fit.FK_fit_power_scaled(p_in_vals, 0.02, 0, 1)
    plt.plot(p_in_vals, sol)
    print(sol.mean())
    plt.show()
