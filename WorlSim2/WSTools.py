import WSpeeps as cp
import WSParms2 as pm
import numpy as np


def flip(p=0.500):
    '''
    Flips a coin with the given probability.
    p: float 0-1; defualt 0.500 (50%)
    returns: boolean (True or False)
    '''
    return np.random.random() < p
