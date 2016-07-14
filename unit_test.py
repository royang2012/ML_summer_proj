import stock_load as sl
import technical_cal as tc
import pandas as pd
import numpy as np
from sklearn import linear_model
import heapq


def prediction(model, testFeature):
    return np.dot(model, testFeature)

# Download data from Jan 2008 to Jan 2015
multiStockTrain = sl.monthlyLoad(1, 2008, 1, 2015)
stockNum = 2#len(multiStockTrain)
coefficient = np.zeros((stockNum, 29))
for i in range(0, stockNum):
    # Construct the training data array
    stockData = tc.technicalCal(multiStockTrain[i])
    (xTrain, yTrain) = tc.featureExt(stockData)

    # train the generalized linear model
    clf = linear_model.LinearRegression()
    clf.fit(xTrain, yTrain)
    coefficient[i, :] = clf.coef_
# print xTrain.shape
# print yTrain.shape
# download testing data
predictionReturn = np.zeros(stockNum)
testStartMonth = 5
testStartYear = 2015
testEndMonth = 5
testEndYear = 2016
testSpan = 12*(testEndYear-testStartYear) + testEndMonth - testStartMonth
monthlyReturn = np.zeros(testSpan)

multiStockTest = sl.monthlyLoad(testStartMonth, testStartYear-1, testEndMonth, testEndYear)
priceDf = pd.DataFrame(np.zeros((testSpan, stockNum)))

for i in range(0, stockNum-1):
    for j in range(0, testSpan):
        priceDf.set_value(j, i, multiStockTest[i].Close[j+12])
percentDf = priceDf.pct_change(axis=0)

for j in range(1, testSpan):
    for i in range(0, stockNum):
        stockData = tc.technicalCal(multiStockTest[i])
        (xTest, yTest) = tc.featureExt(stockData)
        predictionReturn[i] = prediction(coefficient[i,:], xTest[i, :])
    indices = heapq.nlargest(10, range(len(predictionReturn)), predictionReturn.take)
    monthlyReturn[j] = percentDf.ix[j, indices].mean()

print monthlyReturn


