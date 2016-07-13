import stock_load as sl
import technical_cal
import pandas as pd
import numpy as np
# Download data from Jan 2008 to Jan 2015
multiStock = sl.monthlyLoad(1, 2008, 1, 2015)
stockNum = len(multiStock)
monthNum = len(multiStock[0].Date)
# Construct the training data array
featureNum = 29
x = np.zeros((monthNum-13, featureNum))
y = np.zeros((monthNum-13, 1))
stockData = technical_cal.technicalCal(multiStock[0])

for j in range(12, monthNum-1):
    x[j-12, :] = np.array(stockData.ix[j, 6:35].as_matrix())
    y[j-12] = stockData['Close'].ix[j]

print y

# stockData = technical_cal.technicalCal(multiStock[0])
# z = np.array(stockData.ix[1, 6:36].as_matrix())
# print z
# print z.shape