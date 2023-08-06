import collections


def normal_end(file):
    for line in tail(file, 20):
        if "General timing and accounting informations" in line:
            return True
    return False


def converged(oszicar, outcar, tol=1.0e-7):
    with open(outcar) as f:
        if not normal_end(f):
            return False

    with open(oszicar) as f:
        t = tail(f, 2)
        second_to_last = next(t)
        last = next(t)

    try:
        ediff = float(second_to_last.split()[3])
    except ValueError:
        return False

    return abs(ediff) < tol and "F=" in last


def tail(it, n):
    return iter(collections.deque(it, maxlen=n))
