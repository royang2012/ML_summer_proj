import trade_model
import pandas as pd
import numpy as np
# from sklearn import svm
# from sklearn import linear_model
from sklearn.ensemble.forest import RandomForestRegressor
import stockPlot as sp
monthData = trade_model.monthlyModel(1, 2009, 6, 2013, 6, 2012, 6, 2013)
monthData.monthlyDataDownload()
monthData.trainFeaturePre()
# monthData.trainFeaturePreHd()
trainSpan = len(monthData.xTrain[:,0,0]) - monthData.testSpan
# reshapeXtrain = np.zeros((trainSpan*monthData.stockNum, monthData.featureNum))
# reshapeYtrain = np.zeros(trainSpan*monthData.stockNum)
# for i in range(0, monthData.stockNum):
#     reshapeXtrain[i*trainSpan:(i+1)*trainSpan, :] = monthData.xTrain[0:trainSpan, :, i]
#     reshapeYtrain[i*trainSpan:(i+1)*trainSpan] = monthData.yTrain[0:trainSpan, 0, i]

# clf = svm.SVR()
clf = RandomForestRegressor(n_estimators=10)
yearReturn = 1
predictedReturn = np.zeros(monthData.stockNum)
monthlyReturn = np.zeros(monthData.testSpan)
aggReturn = np.zeros(monthData.testSpan+1)
aggReturn[0] = 1
for j in range(0, monthData.testSpan):
    for i in range(0, monthData.stockNum):
        clf.fit(monthData.xTrain[j:trainSpan+j, :, i], monthData.yTrain[j:trainSpan+j, 0, i])
        predictedReturn[i] = clf.predict(monthData.xTest[j, :, i])
    monthlyReturn[j] = monthData.por10Returns(j, predictedReturn)
    yearReturn= yearReturn * (monthlyReturn[j]+1)
    aggReturn[j+1] = aggReturn[j]*(1+monthlyReturn[j])

print monthlyReturn
print 'overall:', yearReturn
sp.portfolioVSspy(6, 2012, 6, 2013, aggReturn[1:])
print aggReturn