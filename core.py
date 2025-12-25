import numpy as np
import cmath

STEP_COUNT = 5000

def calculate(l_val, c_val, r_val, v_val, f_val):
    # l_val : inductance
    # c_val : capacitance
    # r_val : resistance
    # v_val : maximum voltage
    omega = 2 * np.pi * f_val
    x = np.linspace(0, 1, STEP_COUNT)
    v = v_val * np.cos(omega * x)
    zl = 1j * omega * l_val
    return x, v, None, None
