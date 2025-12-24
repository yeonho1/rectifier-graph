import numpy as np

def calculate(l_val, c_val, r_val, v_val):
    # l_val : inductance
    # c_val : capacitance
    # r_val : resistance
    # v_val : maximum voltage
    x = np.linspace(0, np.pi*6, 5000)
    v = v_val * np.cos(x)
    return x, v, None, None
