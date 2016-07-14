import numpy as np

def prediction(model, testFeature):
    return np.dot(model, testFeature)



