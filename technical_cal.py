""""
##
# Created by IntelliJ PyCharm.
# User: ronyang
# Date: 7/2/16
#
"""
import pandas as pd
import technicals
import numpy as np


def technicalCal(stockData):
    """
    - The function first converts the list of stock data into a Dataframe with index 'date',
      'Open', 'Close', 'High', 'Low', 'Aclose' and 'Volume', respectively
    - Then technical are computed and appended to the Dataframe, these technicals will be used
      as input features of the prediction machine
    :param stockData: singleStock instance with data downloaded from Yahoo
    :return: Dataframe that contains raw data and technicals
    """
    dic = {'date': stockData.Date, 'Open': stockData.Open, 'Close': stockData.Close, 'High': stockData.High,
           'Low': stockData.Low, 'Volume': stockData.Vol, 'Aclose': stockData.Aclose}
    df = pd.DataFrame(data=dic)
    df = technicals.MA(df, 6)
    df = technicals.EMA(df, 9)
    df = technicals.MOM(df, 3)
    df = technicals.MOM(df, 6)
    df = technicals.MOM(df, 9)
    df = technicals.ROC(df, 3)
    df = technicals.ATR(df, 6)
    df = technicals.BBANDS(df, 9)
    df = technicals.PPSR(df)
    df = technicals.STOK(df)
    df = technicals.STO(df, 3)
    # # df = technicals.TRIX(df, 6)
    df = technicals.Vortex(df, 9)
    df = technicals.RSI(df, 9)
    df = technicals.ACCDIST(df, 3)
    df = technicals.Chaikin(df)
    df = technicals.MFI(df, 9)
    df = technicals.OBV(df, 9)
    df = technicals.FORCE(df, 3)
    df = technicals.EOM(df, 3)
    df = technicals.CCI(df, 9)
    df = technicals.COPP(df, 2)
    df = technicals.DONCH(df, 9)
    df = technicals.STDDEV(df, 9)
    # df.drop('date', 1)
    # df.drop('Open', 1)
    # df.drop('High', 1)
    # df.drop('Low', 1)
    # df.drop('Volume', 1)
    return df

def featureExt(stockData, featureNum):
    """
    - This function generate feature matrix from technicals
    :param stockData: singleStock instance with data downloaded from Yahoo
    :param featureNum: # of features
    :param x: training feature matrix
    :param y: percentage return
    :return:
    """
    monthNum = len(stockData.index)
    x = np.zeros((monthNum - 13, featureNum))
    y = np.zeros((monthNum - 13, 1))
    # percentage return is calculated from adjusted close of each month
    # feature starts at index #7
    for j in range(12, monthNum - 1):
        y[j - 12] = (stockData['Aclose'].ix[j+1] - stockData['Aclose'].ix[j])/stockData['Aclose'].ix[j]
        x[j - 12, :] = np.array(stockData.ix[j, 7:].as_matrix())
    return x, y

