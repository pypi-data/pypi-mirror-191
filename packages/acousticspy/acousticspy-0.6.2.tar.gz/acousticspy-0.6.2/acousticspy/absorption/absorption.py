import numpy as np

# Gets the absorption coefficient alpha.
#
# f = frequency (Hz)
# ps = local atmospheric pressure (atm)
# T = local temperature (degrees Celsius)
# hr = relative humidity (percent)

# Returns alpha in dB/m
# Reference: https://asa.scitation.org/doi/pdf/10.1121/1.412989

def get_alpha(f,ps,T,hr):

    ps_ref = 1 # atm
    T0 = 293.15 # Kelvin
    T01 = 273.15 # Kelvin
    T = T + 273.15 # Convert temperature to Kelvin

    psat = ps_ref * 10**(-6.8346*(T01/T)**1.261 + 4.6151)
    h = ps_ref * (hr/ps) * psat/ps_ref

    F = f/ps
    FrO = 1/ps_ref * (24 + 4.04e4 * h * (0.02 + h)/(0.391 + h))
    FrN = 1/ps_ref * np.sqrt(T0/T) * (9 + 280*h * np.exp(-4.17*((T0/T)**(1/3) - 1)))

    alpha = F**2 * ps/ps_ref * (
                1.84e-11*np.sqrt(T/T0) + 
                (T/T0)**(-5/2) * (
                    0.01278 * np.exp(-2239.1/T) / (FrO + F**2/FrO) + 
                    0.1068  * np.exp(-3352  /T) / (FrN + F**2/FrN)
                )
            )

    return alpha * 8.686

def get_alpha_classical(f):
    omega = 2*np.pi*f
    nu = 1.81e-5
    c0 = 343
    gamma = 1.4
    Pr = 0.71

    alpha = omega**2*nu/(2*c0**3) * (4/3 + (gamma -1)/Pr)

    return alpha * 8.686

