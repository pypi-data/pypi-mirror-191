G = 6.674 * (10**-11)  # constant G
import numpy as np


def Gravity(m1: float, m2: float, pos1: np.ndarray, pos2: np.ndarray):
    """Calculate gravitational force between two objects"""

    # setting up radius vector (sun to earth)
    r = pos2 - pos1  # creates the radius vector of sun to earth
    rmag = np.linalg.norm(r)  # normalizes the radius vecotr
    rhat = r / rmag  # unit vector for radius

    # define force object 2 exerts on object 1
    return (G * m1 * m2) / (rmag**2) * rhat
