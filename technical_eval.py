import pandas as pd
import numpy as np
from prediction import prediction
import heapq
dfrm = pd.read_csv('./resources/monthly_2011_2015.csv')
dfrm = dfrm.dropna(axis=1)
diffData = dfrm.ix[:, 2:467].pct_change(axis=0).dropna()
diffData.to_csv('./resources/pct_change.csv')
(rowNum, colNum) = diffData.shape
ret = np.zeros(colNum)
grossRet = np.zeros(12)
totalRet = 1
k = 0
for i in range(rowNum-12, rowNum-0):
    for j in range(0, colNum):
        ret[j] = prediction(diffData.ix[i-25:i-1, j].as_matrix())

    indices = heapq.nlargest(10, range(len(ret)), ret.take)
    print indices
    grossRet[k] = diffData.ix[i, indices].mean()
    print grossRet[k]
    totalRet *= (1+grossRet[k])
    k += 1
print totalRet









