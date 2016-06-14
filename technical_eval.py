import pandas as pd
import numpy as np
from prediction import prediction
import heapq
from sklearn import linear_model
import itertools
dfrm = pd.read_csv('./resources/monthly_2011_2015.csv')
dfrm = dfrm.dropna(axis=1)
diffData = dfrm.ix[:, 2:467].pct_change(axis=0).dropna()
diffData.to_csv('./resources/pct_change.csv')
(rowNum, colNum) = diffData.shape
inFeature = np.zeros((rowNum * colNum, 27))
inReturn = np.zeros(rowNum * colNum)
# Training
k = 0
z = 0
for i in range(rowNum - 36, rowNum - 25):
    for j in range(0, colNum):
        inFeature[k, 0:6] = diffData.ix[i - 6:i - 1, j].as_matrix()
        # inFeature[k, 6:12] = np.dot(inFeature[k, 0:6], inFeature[k, 0:6])
        for x in range(0, 6):
            for y in range(x, 6):
                inFeature[k, 6+z] = inFeature[k, x] * inFeature[k, y]
                z += 1
        inReturn[k] = diffData.ix[i, j]
        z = 0
        k += 1
clf = linear_model.LinearRegression()
clf.fit(inFeature, inReturn)
print inFeature[0:1, 0:28]
print clf.coef_
# Testing
testFeature = np.zeros((colNum, 27))
testReturn = np.zeros(colNum)
ret = np.zeros(colNum)
grossRet = np.zeros(12)
totalRet = 1
k = 0
z = 0
for i in range(rowNum - 24, rowNum - 12):
    for j in range(0, colNum):
        testFeature[j, 0:6] = diffData.ix[i - 6:i - 1, j].as_matrix()
        for x in range(0, 6):
            for y in range(x, 6):
                testFeature[k, 6+z] = testFeature[k, x] * testFeature[k, y]
                z += 1
        z = 0

        testReturn[j] = np.dot(clf.coef_, testFeature[j, 0:27])
    indices = heapq.nlargest(10, range(len(testReturn)), testReturn.take)
    grossRet[k] = diffData.ix[i, indices].mean()
    totalRet *= (1 + grossRet[k])
    k += 1

    # print indices
    # grossRet[k] = diffData.ix[i, indices].mean()
    # print grossRet[k]
    # totalRet *= (1 + grossRet[k])
    # k += 1
print totalRet
print grossRet
