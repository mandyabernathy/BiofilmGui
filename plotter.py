# Mandy Abernathy
# plotter.py

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from scipy.optimize import curve_fit

class Plotter:
    """
    A class for plotting planktonic bacteria growth, and finding the growth
    rate of a bacteria given a series of data points.

    Attributes
    ----------
    t : list
        time points
    y : list
        y-values for every time point

    Methods
    -------
    fit():
        fits exponential curve to the class data
    figure():
        creates a figure plotting the class data
    """

    def __init__(self, t, data):
        """
        Constructs all the necessary attributes for the Plotter object.

        Parameters
        ----------
            t : list
                t-values to be plotted on the x-axis
            data : list
                y-values to be plotted on the y-axis
        """
        self.t = t
        self.datapoints = data

    def fit(self):
        """
        Fits an exponential curve to the data saved in the Plotter object.

        Uses the scipy.optimize.curve_fit function to find a value for k_b
        in the following equation given the saved data points:

            b(t) = (b_0)(e^(k_b*t))

        Returns
        -------
            k_b (float) : best-fit parameter for bacteria growth rate
        """
        k_b, pcov = curve_fit(self.exponential_growth, self.t, self.datapoints)
        return k_b

    def figure(self):
        """
        Creates a matplotlib Figure, which contains a plot of bacteria growth
        versus time, using data stored in the Plotter class.

        Returns
        -------
            figure (Figure) : plot of bacteria growth versus time
        """
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(self.t, self.datapoints, 'ro')
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Bacteria Density (OD)')
        return figure

    def exponential_growth(self, t, k_b):
        """
        Callable function required by fit() that describes exponential growth
        of planktonic bacteria.

            b(t) = (b_0)(e^(k_b*t))

        Returns
        -------
            float : value of b(t) given t.
        """
        # e is declared like this because e from math library raises TypeError in curve_fit
        e = 2.7182818284
        return self.datapoints[0] * pow(e, k_b*t)

if __name__ == '__main__':
    p = Plotter()
    plt.plot(p.t, p.y, 'ro')
    plt.plot(p.t, p.exponential_growth(p.t,0.957))
    plt.show()