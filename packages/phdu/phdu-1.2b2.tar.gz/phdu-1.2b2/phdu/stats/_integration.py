import numpy as np
from numba import njit

def simpson3oct_vec(f, a, b, pre, *args):
    """
    Simpson 3 octaves method.
    Attrs:
        - f:   integrand
        - a:   lower end of integration
        - b:   upper end of integration
        - pre: precision
    """
    num = 3
    In = 0.
    In1 = 100.
    while abs(In - In1) > pre:
        In1 = In
        h = (b-a) / num
        In = 0.
        n = 1
        xgrid = np.linspace(a, b, num+1)
        ygrid = f(xgrid, *args)
        if np.isnan(ygrid).all():
            num += 12
            continue
        for k, y in zip(xgrid, ygrid):
            if k == a:
                In = In + (3/8.)*h*y
            if k == b:
                In = In + (3/8.)*h*y
            elif n == 2:
                In = In + (9*h/8.)*y
            elif n == 3:
                In = In + (9*h/8.)*y
            elif n == 4:
                In = In + (6*h/8.)*y
            n += 1
            if n == 5:
                n = 2
        num += 3
    return In, num-3

@njit
def simpson3oct(f, a, b, pre, *args):
    """
    Simpson 3 octaves method.
    Attrs:
        - f:   integrand
        - a:   lower end of integration
        - b:   upper end of integration
        - pre: precision
    """
    num = 3
    In = 0.
    In1 = 100.
    while abs(In - In1) > pre:
        In1 = In
        h = (b-a) / num
        In = 0.
        n = 1
        for k in np.linspace(a, b, num+1):
            if k == a:
                In = In + (3/8.)*h*f(k, *args)
            if k == b:
                In = In + (3/8.)*h*f(k, *args)
            elif n == 2:
                In = In + (9*h/8.)*f(k, *args)
            elif n == 3:
                In = In + (9*h/8.)*f(k, *args)
            elif n == 4:
                In = In + (6*h/8.)*f(k, *args)
            n += 1
            if n == 5:
                n = 2
        num += 3
    return In, num-3

@njit
def trapecios(f,a,b,pre, *args):
    num = 1
    In = 0.
    In1 = 100.
    while abs(In - In1) > pre:
        In1 = In
        h = (b-a) / num
        In = 0.
        for k in np.linspace(a, b, num+1):
            if k == a:
                In = In + (h/2.)*f(k, *args)
            elif k == b:
                In = In + (h/2)*f(k, *args)
            else:
                In = In + h*f(k, *args)
        num += 1
    return In, num-1