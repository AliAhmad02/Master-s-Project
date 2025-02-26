# function [ alpha ] = FK_absorption(lam,T,F)
#FK_absorption Calculates the FK absorption in GaAs
# Franz-Keldysh calculations from G. E. Stillman, C. M. Wolfe, C. O. Bozler, and J. A. Rossi
# Appl. Phys. Lett. 28, 544 (1976)
# https://doi.org/10.1063/1.88816
#
# Usage:
# alpha = FK_absorption(lam,T,F) 
# lam is the wavelength (can be vector)
# T is the temperature (which sets both index and bandgap of GaAs)
# F is the electric field in V/cm
# alpha is the absorption in 1/cm

# Constants

from calc_gaas_index import gaas_index
from scipy import special
import numpy as np

# Here, k is the "kind" of the airy function
def airy(k: int, z: float) -> float:
    if not isinstance(k, int) or k not in [0, 1, 2, 3]:
        raise ValueError("k must be an integer between 0 and 3.")
    else:
        return special.airy(z)[k]

def FK_absorption(lam: float, x: float, T: float, F:float) -> float:
    n = gaas_index(lam,x,T) # GaAs refractive index (constant)
    mh1 = 0.087 # Light-hole effective mass
    mh2 = 0.45 # Heavy-hole effective mass
    mu1 = 0.0377   
    mu2 = 0.0579
    fkcoeff = 0.58 # Experimental coefficient

    Eg = 1.519-5.405e-4*T**2/(T+204) # Temperature-dependent gap 
    Eph = 1239.84/lam

    beta1 = 1.1e5*(Eg-Eph)*(2*mu1)**(1/3)*F**(-2/3)
    beta2 = 1.1e5*(Eg-Eph)*(2*mu2)**(1/3)*F**(-2/3)

    a1 = (1+1/mh1)*(2*mu1)**(4/3)*(np.abs(airy(1,beta1))**2- beta1*np.abs(airy(0, beta1))**2)
    a2 = (1+1/mh2)*(2*mu2)**(4/3)*(np.abs(airy(1,beta2))**2- beta2*np.abs(airy(0, beta2))**2)

    FKa = (a1+a2)*F**(1/3)*1e4/n
    alpha = fkcoeff*FKa
    return alpha

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import scienceplots
    import matplotlib.pyplot as plt

    from mpl_toolkits.mplot3d import axes3d

    lam = 900 * np.linspace(0.85, 1.5, 400)
    # -10V to 10V over a length of 100 nm, in units of V/cm
    fields = np.linspace(1, 10, 400) * 1e5
    T = 298
    x = 0

    lam_mesh, fields_mesh = np.meshgrid(lam, fields)
    alpha_mesh = FK_absorption(lam_mesh, x, T, fields_mesh)

    plt.style.use("science")

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    plt.plot(lam, FK_absorption(lam, x, T, fields))
    ax.plot_wireframe(lam_mesh, fields_mesh, alpha_mesh)
    ax.set_xlabel(r"Wavelength [$\mu m$]", fontsize=14)
    ax.set_ylabel("Electric field", fontsize=14)
    ax.set_zlabel("Franz keldysh absorption", fontsize=14)
    plt.show()
