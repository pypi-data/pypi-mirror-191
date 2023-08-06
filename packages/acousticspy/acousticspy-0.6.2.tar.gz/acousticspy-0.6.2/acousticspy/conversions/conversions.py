import numpy as np

"""
Convert linear frequency to wavenumber
"""
def f_to_k(f,c = 343):
    return 2*np.pi*f / c

"""
Convert wavenumber to linear frequency
"""
def k_to_f(k,c = 343):
    return k*c/(2*np.pi)
