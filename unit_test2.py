import trade_model
import pandas as pd
import numpy as np
from sklearn import linear_model
# import test
#
#
# test = test.test_class()
# test.test()
# print test.b
monthData = trade_model.monthlyModel(1, 2008, 1, 2015, 5, 2015, 5, 2016)
monthData.monthlyDataDownload()
monthData.trainFeaturePre()
##
# coefficient = np.zeros((monthData.stockNum, monthData.featureNum))
#
# for i in range(0, monthData.stockNum):
#     # train the generalized linear model
#     clf = linear_model.LinearRegression()
#     clf.fit(monthData.xTrain[:,:,i], monthData.yTrain[:,:,i])
#     coefficient[i, :] = clf.coef_
#
# predictedReturn = np.zeros(monthData.stockNum)
# monthlyReturn = np.zeros(monthData.testSpan)
# for j in range(1, monthData.testSpan):
#     for i in range(0, monthData.stockNum):
#         predictedReturn[i] = np.dot(coefficient[i, :], monthData.xTest[j, :, i])
#     monthlyReturn[j] = monthData.por10Returns(j,predictedReturn)
#
# print monthlyReturn
##
span = len(monthData.xTrain[:,0,0])
coefficient = np.zeros(monthData.featureNum)
reshapeXtrain = np.zeros((span*monthData.stockNum, monthData.featureNum))
reshapeYtrain = np.zeros(span*monthData.stockNum)
for i in range(0, monthData.stockNum):
    reshapeXtrain[i*span:(i+1)*span,:] = monthData.xTrain[:,:,i]
    reshapeYtrain[i*span:(i+1)*span] = monthData.xTrain[:,0,i]
# train the generalized linear model
clf = linear_model.LinearRegression()
clf.fit(reshapeXtrain, reshapeYtrain)
coefficient = clf.coef_

predictedReturn = np.zeros(monthData.stockNum)
monthlyReturn = np.zeros(monthData.testSpan)
for j in range(1, monthData.testSpan):
    for i in range(0, monthData.stockNum):
        predictedReturn[i] = np.dot(coefficient, monthData.xTest[j, :, i])
    monthlyReturn[j] = monthData.por10Returns(j,predictedReturn)

print monthlyReturn