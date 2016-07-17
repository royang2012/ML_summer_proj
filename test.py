import numpy as np
import pandas as pd

class test_class:
    def __init__(self):
        self.a = np.dstack(([[1,2,3],[2,3,4]],[[3,4,5],[5,6,7]]))
        self.b = pd.DataFrame()

    def test(self):
        temp = np.dstack(([[1,2,3],[2,3,4]],[[3,4,5],[5,6,7]]))
        self.a = np.dstack((self.a,[[6,7,8],[7,8,9]]))
        self.b = pd.DataFrame(np.zeros(3))

a = np.dstack(([[1,2,3],[2,3,4]],[[3,4,5],[5,6,7]]))
b = pd.DataFrame()