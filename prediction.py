import numpy as np


def prediction(pastData):
    return np.mean(pastData[14:23])
