## The canonical refractive index generator. By courtesy of Niels Gregersen
## and based on Gehrsitz et al., J. Appl. Phys. 87, 7825 (2000).

# lam in nm
# x is the molefraction of Al: Al(x)Ga(1-x)As
# T is the temperature in Kelvin
# Without arguments it makes a plot for GaAs at 10K
import numpy as np

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

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import scienceplots

    lam = 900 * np.linspace(0.85, 1.5, 400)
    T = 298
    x = 0
    plt.style.use("science")
    plt.plot(lam, gaas_index(lam, x, T))
    plt.xlabel(r"Wavelength [$\mu m$]", fontsize=14)
    plt.ylabel("Refractive index", fontsize=14)
    plt.show()
