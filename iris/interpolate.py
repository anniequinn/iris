import math
import numpy as np


class Bezier:
    """Methods for performing Bezier interpolation."""

    @staticmethod
    def binomial(n, k):
        """Calculate the binomial coefficient."""
        return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

    @staticmethod
    def interpolate(col_arr, n_out=None):
        """Perform Bezier interpolation on 2D array of colours, `col_arr`."""
        n_in = col_arr.shape[0]
        interp_arr = np.zeros((n_out if n_out else n_in, 3))

        # Calculate interpolation steps if n_out is specified
        if n_out:
            t_steps = np.linspace(0, 1, n_out, endpoint=False)

        coefficients = [Bezier.binomial(n_in - 1, k) for k in range(n_in)]

        # Perform interpolation, use interpolation steps if n_out is specified
        for i, t in enumerate(t_steps if n_out else range(n_in)):
            interp_arr[i] = sum(
                coefficients[k] * (1 - t) ** (n_in - 1 - k) * t**k * col_arr[k]
                for k in range(n_in)
            )

        return interp_arr