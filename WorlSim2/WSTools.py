import WSPerson as cp
import WSParms2 as pm
import numpy as np


def Pheromon(x, y):
    mdna = x
    fdna = y
    herph = 0
    hisph = 0

    if fdna[2] == pm.Biton and fdna[3] == pm.Biton:
        herph = 3
    elif fdna[2] == pm.Biton:
        herph = 1
    elif fdna[3] == pm.Biton:
        herph = 2

    if mdna[2] == pm.Biton and mdna[3] == pm.Biton:
        hisph = 3
    elif mdna[2] == pm.Biton:
        hisph = 1
    elif mdna[3] == pm.Biton:
        hisph = 2

    return hisph, mdna, herph, fdna


def flip(p=0.5):
    """Flips a coin with the given probability.
        p: float 0-1; defualt 0.5 (50%)
        returns: boolean (True or False)
    """
    return np.random.random() < p
