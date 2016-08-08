""""
##
# Created by IntelliJ PyCharm.
# User: ronyang
# Date: 7/11/16
#
- This function test the monthly return prediction model. For simplification, only three features(3m, 6m, 9m momentum)
  are used.
- Random forest regressor is used
"""

import trade_model
import numpy as np
from sklearn.ensemble.forest import RandomForestRegressor
import stockPlot as sp

# Initiate the monthly trade object
monthData = trade_model.monthlyModel(1, 2008, 6, 2016, 6, 2011, 6, 2016)
# Download data from Yahoo finance
monthData.monthlyDataDownload()
# Pre-processing of training an testing data
monthData.trainFeaturePre()
# Read pre-processed data from hard drive
# monthData.trainFeaturePreHd()
# Number of training months
trainSpan = len(monthData.xTrain[:,0,0]) - monthData.testSpan
# Initiate a random forest regressor
clf = RandomForestRegressor(n_estimators=300)
#d
totalReturn = 1
predictedReturn = np.zeros(monthData.stockNum)
monthlyReturn = np.zeros(monthData.testSpan)
aggReturn = np.zeros(monthData.testSpan+1)
aggReturn[0] = 1
# rolling training and testing
for j in range(0, monthData.testSpan):
    for i in range(0, monthData.stockNum):
        clf.fit(monthData.xTrain[j:trainSpan+j, :, i], monthData.yTrain[j:trainSpan+j, 0, i])
        predictedReturn[i] = clf.predict(monthData.xTest[j, :, i])
    monthlyReturn[j] = monthData.por10Returns(j, predictedReturn)
    totalReturn = totalReturn * (monthlyReturn[j]+1)
    aggReturn[j+1] = aggReturn[j]*(1+monthlyReturn[j])

print monthlyReturn
print 'overall:', totalReturn
sp.portfolioVSspy(6, 2011, 6, 2016, aggReturn[1:])
