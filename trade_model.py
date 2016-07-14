import technical_cal as tc
import pandas as pd
import numpy as np
import heapq
from download_yahoo import singleStock
import csv
import pickle

class monthlyModel:
    def __init__(self, trainMonth1,trainYear1,trainMonth2, trainYear2, testMonth1, testYear1,
                 testMonth2, testYear2):
        # time variables initialization
        self.trainMonth1 = trainMonth1
        self.trainYear1 = trainYear1
        self.trainMonth2 = trainMonth2
        self.trainYear2 = trainYear2
        self.testMonth1 = testMonth1
        self.testYear1 = testYear1
        self.testMonth2 = testMonth2
        self.testYear2 = testYear2

        self.multiStockTrain = []
        self.multiStockTest = []
        self.stockNum = 0
        self.featureNum = 29

        self.xTrain = np.zeros(1)
        self.yTrain = np.zeros(1)
        self.priceDf = pd.DataFrame()
        self.percentDf = pd.DataFrame()
        self.testSpan = 12*(testYear2-testYear1) + testMonth2 - testMonth1

    def monthlyDataDownload(self):
        self.multiStockTrain = []
        self.multiStockTest = []
        with open('./resources/SnP500_his.csv', 'rb') as f:
            reader = csv.reader(f)
            ticker_list = list(reader)
        for tickers in ticker_list:
            tickerstring = tickers[0]
            s1 = singleStock(tickerstring, self.trainMonth1, 1, self.trainYear1,
                             self.trainMonth2, 28, self.trainYear2, 'm')
            s1.loading()
            self.multiStockTrain.append(s1)
            s2 = singleStock(tickerstring, self.testMonth1, 1, self.testYear1-1,
                             self.testMonth2, 28, self.testYear2, 'm')
            s2.loading()
            self.multiStockTest.append(s2)
            self.stockNum = len(self.multiStockTrain)
        f1 = open('./resources/multiStockTrain', 'w')
        pickle.dump(self.multiStockTrain, f1)
        f2 = open('./resources/multiStockTest', 'w')
        pickle.dump(self.multiStockTrain, f2)

        return self.stockNum


    def trainFeaturePre(self):
        coefficient = np.zeros((self.stockNum, self.stockNum))
        stockData = tc.technicalCal(self.multiStockTrain[0])
        (xTrains, yTrains) = tc.featureExt(stockData)
        self.xTrain = xTrains
        self.yTrain = yTrains
        for i in range(1, self.stockNum):
            # Construct the training data array
            stockData = tc.technicalCal(self.multiStockTrain[i])
            (xTrains, yTrains) = tc.featureExt(stockData)
            self.xTrain = np.dstack((self.xTrain, xTrains))
            self.yTrain = np.dstack((self.yTrain, yTrains))
        for i in range(0, self.stockNum - 1):
            for j in range(0, self.testSpan):
                self.priceDf.set_value(j, i, self.multiStockTest[i].Close[j + 12])
        self.percentDf = self.priceDf.pct_change(axis=0)
        return self.xTrain.shape, self.yTrain.shape

    def por10Returns(self, monthCount, predictedReturn):
        indices = heapq.nlargest(10, range(len(predictedReturn)), predictedReturn.take)
        return self.percentDf.ix[monthCount, indices].mean()
