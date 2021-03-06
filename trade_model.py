""""
##
# Created by IntelliJ PyCharm.
# User: ronyang
# Date: 7/2/16
#
"""
import technical_cal as tc
import pandas as pd
import numpy as np
import heapq
from download_yahoo import singleStock
import csv
import cPickle

class monthlyModel:
    """
    - This class download, process and store the stock data for monthly trading model
    .. fields::
        trainMonth1: train starting month
        trainYear1: train starting year
        trainMonth2: train ending month
        trainYear2: train ending year
        multiStockTrain: list of singleStock instances
        xTrain: 3D numpy array of training feature matrix; axis 0: time, axis 1: features, axis 2: companies
        yTrain: 3D numpy array of percentage return; axis 0: time, axis 1: % return, axis 2: companies
        xTest: xTrain
        yTest: yTrain
        priceDf: dataframe of yTest
        indices: list of indices that corresponds to 10 greatest predicted returns
    """
    def __init__(self, trainMonth1,trainYear1,trainMonth2, trainYear2, testMonth1, testYear1,
                 testMonth2, testYear2):
        #
        self.trainMonth1 = trainMonth1
        self.trainYear1 = trainYear1
        self.trainMonth2 = trainMonth2
        self.trainYear2 = trainYear2
        self.testMonth1 = testMonth1
        self.testYear1 = testYear1
        self.testMonth2 = testMonth2
        self.testYear2 = testYear2
        #
        self.multiStockTrain = []
        self.stockNum = 0
        self.featureNum = 0

        self.xTrain = np.zeros(1)
        self.yTrain = np.zeros(1)
        self.priceDf = pd.DataFrame()
        self.xTest = np.zeros(1)
        self.yTest = np.zeros(1)
        self.percentDf = pd.DataFrame()

        self.trainSpan = 12*(trainYear2-trainYear1) + trainMonth2 - trainMonth1
        self.testSpan = 12*(testYear2-testYear1) + testMonth2 - testMonth1

        self.indices = []

    def monthlyDataDownload(self):
        """
        - This function call singleStock class
        - All fields are reversed to make column index consistent with chronosequence
        :return:
        """
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
            s1.Aclose.reverse()
            s1.Close.reverse()
            s1.Date.reverse()
            s1.Open.reverse()
            s1.High.reverse()
            s1.Low.reverse()
            self.multiStockTrain.append(s1)
            self.stockNum = len(self.multiStockTrain)


        return self.multiStockTrain[0]


    def trainFeaturePre(self):
        """
        - This function pre-process the training and testing data, generate numpy arrays
        :return:
        """
        stockData = tc.technicalCal(self.multiStockTrain[0])
        self.featureNum = stockData.shape[1]-7
        (xTrains, yTrains) = tc.featureExt(stockData, self.featureNum)
        self.xTrain = xTrains
        self.yTrain = yTrains
        for i in range(1, self.stockNum):
            # Construct the training data array
            stockData = tc.technicalCal(self.multiStockTrain[i])
            (xTrains, yTrains) = tc.featureExt(stockData, self.featureNum)
            self.xTrain = np.dstack((self.xTrain, xTrains))
            self.yTrain = np.dstack((self.yTrain, yTrains))
        # self.xTest = np.zeros((self.testSpan, self.featureNum, self.stockNum))
        # self.yTest = np.zeros((self.testSpan, 1, self.stockNum))
        self.xTest = self.xTrain[self.trainSpan - self.testSpan -12:self.trainSpan-12, :, :]
        self.yTest = self.yTrain[self.trainSpan - self.testSpan -12:self.trainSpan-12, 0, :]
        # stockData = tc.technicalCal(self.multiStockTest[0])
        # (xTests, yTests) = tc.featureExt(stockData, self.featureNum)
        # self.xTest = xTests
        # self.yTest = yTests
        # for i in range(1, self.stockNum):
        #     stockData = tc.technicalCal(self.multiStockTest[i])
        #     (xTests, yTests) = tc.featureExt(stockData, self.featureNum)
        #     self.xTest = np.dstack((self.xTest, xTests))
        #     self.yTest = np.dstack((self.yTest, yTests))
        #     # for j in range(0, self.testSpan):
        #         # self.priceDf.set_value(j, i, self.multiStockTest[i].Close[j + 12])
        #
        self.percentDf = pd.DataFrame(self.yTest)

        # save to file
        cPickle.dump(self.xTrain, open("./resources/multiStockTrainx.pkl", "wb"))
        cPickle.dump(self.yTrain, open("./resources/multiStockTrainy.pkl", "wb"))
        cPickle.dump(self.xTest, open("./resources/multiStockTestx.pkl", "wb"))
        cPickle.dump(self.yTest, open("./resources/multiStockTesty.pkl", "wb"))
        return self.xTrain.shape, self.yTrain.shape

    def trainFeaturePreHd(self):
        """
        - This function read saved data from hard drive
        :return:
        """
        self.xTrain = cPickle.load(open("./resources/multiStockTrainx.pkl", "rb"))
        self.yTrain = cPickle.load(open("./resources/multiStockTrainy.pkl", "rb"))
        self.xTest = cPickle.load(open("./resources/multiStockTestx.pkl", "rb"))
        self.yTest = cPickle.load(open("./resources/multiStockTesty.pkl", "rb"))

        self.featureNum = self.xTrain.shape[1]
        self.stockNum = self.xTrain.shape[2]
        self.percentDf = pd.DataFrame(self.yTest)

    def por10Returns(self, monthCount, predictedReturn):
        """
        - This function find the 10-stock portfolio based on prediction
        :param monthCount: count of testing month
        :param predictedReturn: percentage return prediction
        :return: mean of the actual percentage return in portfolio
        """
        self.indices = heapq.nlargest(10, range(len(predictedReturn)), predictedReturn.take)
        return self.percentDf.ix[monthCount, self.indices].mean()
