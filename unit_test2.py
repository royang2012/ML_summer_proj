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

coefficient = np.zeros((monthData.stockNum, monthData.featureNum))
print monthData.xTrain[0][0][:]
print monthData.xTrain[0][:][0]
# for i in range(0, monthData.stockNum):
#     # train the generalized linear model
#     clf = linear_model.LinearRegression()
#     clf.fit(monthData.xTrain[:][:][i], monthData.yTrain[:][:][i])
#     coefficient[i, :] = clf.coef_
#
# print coefficient.shape

