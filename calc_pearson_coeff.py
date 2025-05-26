import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from colorama import Fore, init

init(autoreset=True)

def sigma(x: list, exp=1):
    x = np.array(x)
    return np.sum(x ** exp)

def and_sigma(x: list, y: list):
    return np.dot(x, y)

def get_order_pair_no(x, y):
    return min(len(x), len(y))

def calc_pearson_coeff_manual(x, y):
    n = get_order_pair_no(x, y)
    x = x[:n]
    y = y[:n]
    sigma_x = sigma(x)
    sigma_y = sigma(y)
    sigma_xy = and_sigma(x, y)
    sigma_x_square = sigma(x, exp=2)
    sigma_y_square = sigma(y, exp=2)

    numerator = (n * sigma_xy) - (sigma_x * sigma_y)
    denominator = (((n * sigma_x_square) - (sigma_x ** 2)) * ((n * sigma_y_square) - (sigma_y ** 2))) ** 0.5
    coeff = numerator / denominator
    return coeff

def calc_pearson_coeff(x, y, supress=False):
    if len(x) == len(y):
        corr_matrix = np.corrcoef(x, y)
        return corr_matrix[0, 1]
    else:
        if not supress:
            print(Fore.YELLOW + "[WARNING] " + """Both arrays are not of equal size, truncating largest one to fit size of smaller.\nThis will affect the result, consider padding or try a different approach.""")
        return calc_pearson_coeff_manual(x, y)

def calculate_deviation_graph(x, y, factor=0.3):
    print("Set x to constant and y to be changing values")
    constants = []
    varying_axis = []
    y = y.copy()  # Avoid mutating original list
    length_stop = int(len(y) * factor)
    print("STOP SET TO", length_stop)

    while len(y) > max(length_stop, 3):
        varying_axis.append(len(y))
        constants.append(calc_pearson_coeff(x, y, supress=True))
        y.pop()

    # Reverse x-axis for a "leftward" plot
    varying_axis.reverse()
    constants.reverse()

    fig, ax = plt.subplots()
    ax.set_title("Effect of Truncating Y on Pearson Correlation")
    ax.set_xlabel("Length of Y (truncated →)")
    ax.set_ylabel("Pearson Correlation Coefficient")
    ax.plot(varying_axis, constants, marker='o', color="blue", label="Correlation")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
    ax.legend()
    ax.grid(True)
    ax.invert_xaxis()  # Reverse X-axis to show truncation direction
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # np.random.seed(42)  # for reproducibility
    # x = np.arange(1, 101)  # [1, 2, ..., 100]
    # y = 3 * x + np.random.normal(0, 10, size=100)  # Strong linear relation with noise

    # x = x.tolist()
    # y = y.tolist()
    # calculate_deviation_graph(x, y, factor=0.01)

    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [-1, -4, -9, -16, -25, -50, -69, -85, -101]
    
    print(calc_pearson_coeff(x, y))

