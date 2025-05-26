from sympy import symbols, diff, solve, lambdify
from scipy.stats import norm, skew, kurtosis
import numpy as np
import matplotlib.pyplot as plt
import math
import os

def nth_term(start: int, diff: int, n: int) -> int:
    """Returns the n-th term of an arithmetic series."""
    return start + (n - 1) * diff

def nth_sum(start: int, diff: int, n: int, last_term: int = None) -> float:
    """Returns the sum of the first n terms of an arithmetic series.
    
    If last_term is provided, uses formula: (n / 2) * (a + l)
    Else uses: (n / 2) * (2a + (n - 1)d)
    """
    if last_term is not None:
        return (n / 2) * (start + last_term)
    else:
        return (n / 2) * (2 * start + (n - 1) * diff)

def get_symbol(expr):
    from collections import Counter
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    try:
        filtered = [ch for ch in expr.lower() if ch in alpha]
    except TypeError:
        return None
    
    if not filtered:
        return None  # No valid symbol
    
    freq = Counter(filtered)
    # Return the most frequent symbol
    return freq.most_common(1)[0][0]

def get_crit(expr):
    variable = get_symbol(expr)
    if variable is None:
        raise ValueError("No variable  found in expression")
    var = symbols(variable)
    first_deriv = diff(expr, var)
    second_deriv = diff(first_deriv, var)

    crit_pts = solve(first_deriv, var)

    results = []
    for point in crit_pts:
        val = second_deriv.subs(var, point)
        if val > 0:
            nature = "Minimum"
        elif val < 0:
            nature = "Maximum"
        else:
            nature = "Inconclusive"
        results.append((point.evalf(), nature))
    return results

def nPr(n:int, r:int) -> int:
    """Calculate number of permutations (nPr) — arrangements of r items from n."""
    num = math.factorial(n)
    if not(0 <= r <= n):
        raise ValueError("r must lie between 0 and {}".format(n))
    den = math.factorial(n - r)
    return num // den

def plot_bell_curve_from_data(
    data,
    xlabel='Value',
    ylabel='Density',
    title='Bell Curve',
    save_path=None,
    show=True
):
    """
    Plot a smooth bell curve from raw numeric data with mean and ±1σ, ±2σ, ±3σ.
    Displays mean, std dev, skewness, kurtosis.
    Optionally saves the plot.

    Args:
        data (list): Raw numeric data.
        xlabel (str): Label for x-axis.
        ylabel (str): Label for y-axis.
        title (str): Plot title.
        save_path (str): Where to save the plot (e.g., 'images/plot.png').
        show (bool): Whether to display the plot (default: True).
    """
    data = np.array(data)
    mu, sigma = np.mean(data), np.std(data)
    skewness = skew(data)
    kurt = kurtosis(data)

    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    y = norm.pdf(x, mu, sigma)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', lw=2, label='Normal Distribution')

    # Mean line
    plt.axvline(mu, color='red', linestyle='--', label=f'Mean = {mu:.2f}')

    # Shade and mark ±1σ, ±2σ, ±3σ
    colors = ['#d0ebff', '#a5d8ff', '#74c0fc']  # lighter to darker blue
    for i in range(1, 4):
        x_fill = np.linspace(mu - i*sigma, mu + i*sigma, 1000)
        y_fill = norm.pdf(x_fill, mu, sigma)
        plt.fill_between(x_fill, y_fill, color=colors[i-1], alpha=0.4, label=f'±{i}σ')

    # Annotations
    plt.text(mu, max(y) * 0.95, f"μ = {mu:.2f}\nσ = {sigma:.2f}\nskew = {skewness:.2f}\nkurtosis = {kurt:.2f}",
             horizontalalignment='left', verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Plot saved to: {save_path}")

    if show:
        plt.show()
    else:
        plt.close()

#if __name__ == "__main__":
    #print(nth_term(1, 20, 98))
    #print(nth_sum(1, 1, 10))
    #print(get_crit("3 - 6 * 2 - 9 + 15"))
    #data = [2, 2, 3, 3, 3, 4, 4, 5, 6, 10, 20, 30, 50, 70, 100]
    #plot_bell_curve_from_data(data, xlabel='Purchases', ylabel='Density', title='Customer Purchases Distribution')