# Mandy Abernathy
# model.py

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import numpy as np

class Model:
    """
    A class for modeling bacterial biofilm growth according to a logistic
    equation that also describes inhibitory treatments.

    Attributes
    ----------
    t : array
        time points
    t_span : list
        contains the time span of the model, [t0, t24]
    k_b : float
        bacteria growth rate
    initial_state : list 
        initial amount of biofilm, [B_0]
    B_max : float
        maximum amount of biofilm that can grow
    agent_MIC : float
        minimum inhibitory concentration of antibiotic
    agent_conc : float
        concentration of antibiotic treatment

    Methods
    -------
    solve():
        solves initial value problem for differential equation for biofilm growth
    figure():
        creates a figure plotting biofilm growth
    """

    def __init__(self, growthrate, initcond, maxvalue, abx_mic, abx_conc):
        """
        Constructs all the necessary attributes for the Model object.

        Parameters
        ----------
            growthrate : float
                describes the growth rate of bacteria
            initcond : float
                initial amount of biofilm 
            maxvalue : float
                maximum amount of biofilm that can be reached
            abx_mic : int
                minimum inhibitory concentration of antibiotic which describes
                the lowest concentration of antibiotic that will inhibit bacteria
                growth, expressed in micrograms per ml
            abx_conc : int
                concentration of antibiotic applied to the biofilm,
                expressed in micrograms per ml
        """
        self.t = np.linspace(0, 24, 25)
        self.t_span = [0, 24]
        self.k_b = growthrate
        self.initial_state = [initcond]
        self.B_max = maxvalue
        self.agent_MIC = abx_mic
        self.agent_conc = abx_conc
        self.y = self.solve()

    def solve(self):
        """
        Solves an initial value problem for a differential equation describing
        logistic biofilm growth, given values saved in the Model object.

        Uses the scipy.integrate.solve_ivp function which integrations a DE
        given an initial value:
            dy / dt = f(t, y)
            y(t0) = y0

        Returns
        -------
            List of y-values which are the solution to the DE at each time point.
        """
        solution = solve_ivp(self.logistic_growth, self.t_span, self.initial_state, t_eval=self.t)
        return solution.y[0]

    def figure(self):
        """
        Creates a matplotlib Figure, which contains a plot of biofilm growth 
        versus time, using data stored in the Model class.

        Returns
        -------
            figure (Figure) : plot of biofilm growth versus time
        """
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(self.t, self.y)
        ax.set_xlabel('Time (hours)')
        ax.set_ylabel('Biofilm (OD)')
        return figure

    def logistic_growth(self, t, B):
        """
        Callable function required by solve() that describes various stages of biofilm
        growth and takes into account the decrease in growth due to nutrient and 
        environmental limitations. [1]

        The component describing agent interaction assumes that the action of the
        agent is proportional to the product agent and biofilm. This interaction
        depends on the antibiotic's MIC and concentration.

            g(t, B) = (k_b)(B)(1 - B/B_max) - (theta)(C)(B)
            where: theta = k_b / MIC

        Returns
        -------
            float : value of g(t,B) given t, B, and biofilm constants saved in Model object.
        
        References
        ----------
        [1] D. Verotta, J. Haagensen, A. Spormann, K. Yang, "Mathematical Modeling
        of Biofilm Structures Using COMSTAT Data", Computational and Mathematical 
        Methods in Medicine, Article ID 7246286, 2017.
        """
        theta = 0.0 # constant that describes agent interaction with biofilm
        if self.agent_MIC != 0:
            theta = self.k_b / float(self.agent_MIC)
        return (self.k_b * B) * (1 - (B / self.B_max)) - (theta * self.agent_conc * B)

if __name__ == '__main__':
    m = Model(0.957, 0.002, 1.75, 0, 0)
    plt.plot(m.t, m.y)
    plt.show()

