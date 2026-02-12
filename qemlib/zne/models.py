import numpy as np
from scipy.optimize import curve_fit


# Extrapolation models

def linear_model(x, a, b):
    return a * x + b


def quadratic_model(x, a, b, c):
    return a * x**2 + b * x + c


def exponential_model(x, a, b, c):
    return a * np.exp(-b * x) + c


# ZNE extrapolation

def extrapolate(xdata, ydata, method="linear"):
    """
    Perform zero-noise extrapolation on expectation values.

    Parameters
    ----------
    xdata : array-like
        Noise scaling factors.
    ydata : array-like
        Expectation values measured at the scale factors.
    method : str
        The extrapolation model to use:'linear', 'quadratic', or 'exponential'.

    Returns
    -------
    dict
        {
            "zero_noise_value": float, Extrapolated value at scale = 0
            "fit_params": tuple, Fitted model parameters
            "fit_function": callable, The fitted model function
        }
    """
    xdata = np.asarray(xdata)
    ydata = np.asarray(ydata)

    if method == "linear":
        popt, _ = curve_fit(linear_model, xdata, ydata)
        zero = linear_model(0, *popt)
        fn = linear_model

    elif method == "quadratic":
        popt, _ = curve_fit(quadratic_model, xdata, ydata)
        zero = quadratic_model(0, *popt)
        fn = quadratic_model

    elif method == "exponential":
        popt, _ = curve_fit(
            exponential_model,
            xdata,
            ydata,
            p0=(1.0, 0.1, ydata[-1]),
            maxfev=5000,
        )
        zero = exponential_model(0, *popt)
        fn = exponential_model

    else:
        raise ValueError(f"Unknown method '{method}'")

    return {
        "zero_noise_value": zero,
        "fit_params": popt,
        "fit_function": fn,
    }
