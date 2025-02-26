# function [ z ] = fk_fitmodel( u,c,b,d)
# FK_FITMODEL Summary of this function goes here
#   Detailed explanation goes here
# y=u(:,1)
# x=u(:,2)

import numpy as np
from FK_absorption import FK_absorption
from scipy.optimize import root_scalar, fsolve
import matplotlib.pyplot as plt


# def FK_fit(lam: float, x: float, T: float, V_d: float, a: float, b: float) -> float:
#     # Na=1e25
#     # Nd=2e24
#     # eps0 = 8.85e-12
#     # er = 12
#     # q = 1.6e-19
#     # d0 = 100e-9
#     # xd = 1e2*sqrt(d0**2+2*er*eps0/q*(Na+Nd)/(Na*Nd)*(1.4-x))
#     # We do things in nanometers first then convert to centimeters
#     # to avoid floating point issues. 795.5 is in units nm²/V
#     depletion_width = 1e-7 * np.sqrt(1e4 + 795.5 * (1.4 - V_d))
#     return a * FK_absorption(lam, x, T, -(V_d - 1.4) / depletion_width) + b


def FK_fit(lam: float, x: float, T: float, V_d: float) -> float:
    # Na=1e25
    # Nd=2e24
    # eps0 = 8.85e-12
    # er = 12
    # q = 1.6e-19
    # d0 = 100e-9
    # xd = 1e2*sqrt(d0**2+2*er*eps0/q*(Na+Nd)/(Na*Nd)*(1.4-x))
    # We do things in nanometers first then convert to centimeters
    # to avoid floating point issues. 795.5 is in units nm²/V
    depletion_width = 1e-7 * np.sqrt(1e4 + 795.5 * (1.4 - V_d))
    return FK_absorption(lam, x, T, -(V_d - 1.4) / depletion_width)


# def FK_fit_power(
#     P_in: float,
#     eta: float,
#     R: float,
#     L: float,
#     lam: float,
#     x: float,
#     T: float,
#     V_app: float,
#     a: float,
#     b: float,
# ):
#     alphas = []
#     for power in P_in:
#         func = (
#             lambda alpha: FK_fit(
#                 lam, x, T, V_app + power * eta * R * (1 - np.exp(-alpha * L)), a, b
#             )
#             - alpha
#         )
#         alpha = fsolve(func, 1000)[0]
#         # alpha = root_scalar(func, bracket=[0, 1e6], method='brentq').root
#         alphas.append(alpha)

#     alphas = np.array(alphas)
#     return P_in * np.exp(-L * alphas), alphas


def FK_fit_power(
    P_in: float,
    eta: float,
    R: float,
    L: float,
    lam: float,
    x: float,
    T: float,
    V_app: float,
    alpha_0: float,
):
    alphas = []
    for power in P_in:
        func = (
            lambda alpha: FK_fit(
                lam, x, T, V_app + power * eta * R * (1 - np.exp(-alpha * L))
            )
            + alpha_0
            - alpha
        )
        alpha = fsolve(func, 1000)[0]
        # alpha = root_scalar(func, bracket=[0, 1e6], method='brentq').root
        alphas.append(alpha)

    alphas = np.array(alphas)
    return P_in * np.exp(-L * alphas), alphas


if __name__ == "__main__":
    p_in_vals = np.linspace(0, 100, 500)
    # Power in muW, eta in A/W, R in Mohm, L in cm, lambda in nm, T in K, V_app in V
    sol, alphas = FK_fit_power(p_in_vals, 0.02, 1, 3.5e-3, 930, 0.3, 298, -4, 0)
    plt.plot(p_in_vals, sol)
    print(sol.mean())
    # plt.plot(p_in_vals, alphas)
    plt.show()
