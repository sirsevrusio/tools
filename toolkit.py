from sympy import symbols, diff, solve, lambdify

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

if __name__ == "__main__":
    #print(nth_term(1, 20, 98))
    #print(nth_sum(1, 1, 10))
    print(get_crit("3 - 6 * 2 - 9 + 15"))