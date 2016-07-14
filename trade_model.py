import stock_load as sl
import technical_cal as tc
import pandas as pd
import numpy as np
from sklearn import linear_model
import heapq
from download_yahoo import singleStock
import csv

class monthlyModel:
    def __init__(self, trainMonth1,trainYear1,trainMonth2, trainYear2, testMonth1, testYear1,
                 testmonth2, testyear2):
        # time variables initialization
        self.trainMonth1 = trainMonth1
        self.trainYear1 = trainYear1
        self.trainMonth2 = trainMonth2
        self.trainYear2 = trainYear2
        self.testMonth1 = testMonth1
        self.testYear1 = testYear1
        self.testMonth2 = testmonth2
        self.testYear2 = testyear2

        self.multiStockTrain = []
        self.multiStockTest = []
        self.stockNum = 0
        self.featureNum = 29

        slef.xTrain =

    def monthlyDataDownload(self):
        self.multiStockTrain = []
        self.multiStockTest = []
        with open('./resources/SnP500_his.csv', 'rb') as f:
            reader = csv.reader(f)
            ticker_list = list(reader)
        for tickers in ticker_list:
            tickerstring = tickers[0]
            s1 = singleStock(tickerstring, self.trainMonth1, 1, self.trainYear1,
                             self.trainMonth2, 1, self.trainYear2, 'm')
            s1.loading()
            self.multiStockTrain.append(s1)
            s2 = singleStock(tickerstring, self.testMonth1, 1, self.testYear1,
                             self.testMonth2, 1, self.testYear2, 'm')
            s2.loading()
            self.multiStockTrain.append(s2)
        return self.stockNum

    def trainFeaturePre(self):
        coefficient = np.zeros((self.stockNum, self.stockNum))
        for i in range(0, self.stockNum):
            # Construct the training data array
            stockData = tc.technicalCal(self.multiStockTrain[i])
            (xTrain, yTrain) = tc.featureExt(stockData)
        return xTrain, yTrain

