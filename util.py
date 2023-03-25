import numpy as np
import math

# utilities
def convert_f_to_r(temp):
    return temp + 459.67

def to_rankine(value, _from):
    rankine = 0
    if _from == "k":
        rankine = value * 1.8
    elif _from == "f":
        rankine = value + 459.67
    elif _from == "c":
        rankine = (value + 273.25) * 1.8
    return round(rankine, 2)
    
def to_psi(value, _from):
    psi = 0
    if _from == "kpa":
        psi = value * 0.145038
    elif _from == "atm":
        psi = value * 14.6956
    return round(psi, 2)
        
def calculate_tr(temp, temp_c):
    converted_temp = convert_f_to_r(temp)
    converted_temp_c = convert_f_to_r(temp_c)
    return converted_temp / converted_temp_c

def calculate_b(temp_c, pressure_c):
    converted_temp_c = convert_f_to_r(temp_c)
    return (0.07780 * ((10.732 * converted_temp_c) / (pressure_c)))

def calculate_ac(temp_c, pressure_c):
    converted_temp_c = convert_f_to_r(temp_c)
    return (0.45724 * ((10.732 ** 2)* (converted_temp_c ** 2)) / pressure_c)

def calculate_alpha(w, temp, temp_c):
    tr = calculate_tr(temp, temp_c)
    alpha_half = 1 + (0.37464 + (1.54226 * w) - (0.26992 * (w ** 2))) * (1 - (tr ** 0.5))
    return alpha_half ** 2

def calculate_at(ac, alpha):
    return ac * alpha



# without the need for conversion to rankine
def calculate_tr_no_convert(temp, temp_c):
    return temp / temp_c

def calculate_b_no_convert(temp_c, pressure_c):
    return (0.07780 * ((10.732 * temp_c) / (pressure_c)))

def calculate_ac_no_convert(temp_c, pressure_c):
    return (0.45724 * ((10.732 ** 2)* (temp_c ** 2)) / pressure_c)

def calculate_alpha_no_convert(w, temp, temp_c):
    tr = calculate_tr_no_convert(temp, temp_c)
    alpha_half = 1 + (0.37464 + (1.54226 * w) - (0.26992 * (w ** 2))) * (1 - (tr ** 0.5))
    return alpha_half ** 2

def calculate_at_no_convert(ac, alpha):
    return ac * alpha



# Trial section functions
def cubic_root_calculation_for_PR_EOS(A, B, print_original=False):
    # define coefficents
    a = 1
    b = -(1 - B)
    c = (A - (2*B) - (3*(B ** 2)))
    d = -((A*B) - (B**2) - (B**3))
    
    coefs = [a, b, c, d]
    roots = np.roots(coefs)
    # check for complex numbera and get the real part
    new_roots = []
    if not print_original:
        for number in roots:
            new_roots.append(number.real)
        return new_roots
    else:
        return list(roots)

def filter_out_complex_numbers(numbers_array):
    filtered_numbers = []
    for num in numbers_array:
        if num.imag == 0:
            filtered_numbers.append(num.real)
    return filtered_numbers
    
def get_highest_or_lowest_root(roots, phase):
    try:
        if type(roots) != list or len(roots) == 0:
            raise Exception('The roots have to be a list and not empty')
        else:
            if len(roots) > 1:
                lowest = min(roots)
                highest = max(roots)
                return highest if phase == 'gas' else lowest
            else:
                return roots[0]
    except Exception as error:
        text = f"<div style='color:red'>{error}</div>"
        display(HTML(text))
            

def solve_for_fg_fl(z, B, A, trial_pressure):
    z = z
    B = B
    A = A
    p = trial_pressure
    first_part = math.log(z - B)
    second_part = (A / ((2**1.5)*B))
    numerator = (z + (((2**0.5) + 1) * B))
    denominator = (z - (((2**0.5) - 1) * B))
    log_part = math.log(numerator / denominator)
    f_value = math.exp(z - 1 - first_part - (second_part * log_part)) * trial_pressure
    
    return f_value

# question two utils
# calculate_xj of each component
def calculate_xj(z, k, ng):
    return z / (1 + (ng * (k - 1)))

def calculate_yj(z, k, nl):
    return z / (1 + (nl * ((1/k) - 1)))

def calculate_aT_per_phase(y, aT, kappa):
    """y is an list of the yj or xj, aT is an list of aTj and kappa is a matrix (2D list) of te BIP"""
    n = len(y)
    aT_sum = 0.0
    for i in range(n):
        for j in range(n):
            aT_sum += y[i] * y[j] * ((aT[i] * aT[j])**(0.5)) * (1.0 - (kappa[i][j]))
    return aT_sum

def calcuate_b_per_phase(y, b):
    n = len(y)
    b_sum = 0.0
    for i in range(n):
        b_sum += y[i] * b[i]
    return b_sum

def calculate_A(aT, trial_pressure, sys_temp):
    temp = convert_f_to_r(sys_temp)
    return (aT * trial_pressure) / ((10.732 ** 2) * (temp ** 2))

def calculate_B(b, trial_pressure, sys_temp):
    temp = convert_f_to_r(sys_temp)
    return (b * trial_pressure) / (10.732 * temp)

# no convert
def calculate_A_no_convert(aT, trial_pressure, sys_temp):
    return (aT * trial_pressure) / ((10.732 ** 2) * (sys_temp ** 2))

def calculate_B_no_convert(b, trial_pressure, sys_temp):
    return (b * trial_pressure) / (10.732 * sys_temp)



# miscillenous utilities
def sum_of_a_key_in_list_of_dict(key, list):
    total_sum = 0
    for item in list:
        total_sum += item[key]
    return total_sum

def keys_to_list_of_dict(key, data):
    return {component["component"]: component[key] for component in data}

def update_key_value(data_list, check_value, target_key, new_value):
    for component in data_list:
        if component['component'] == check_value:
            component[target_key] = new_value
            break
