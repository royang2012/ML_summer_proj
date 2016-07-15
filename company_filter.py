import technical_cal as tc
from download_yahoo import singleStock
import pandas as pd
import numpy as np
validCompany = list()
companyList = pd.read_csv('./resources/SnP500History.csv')
rowNum = companyList.shape[0]
for i in range(0, rowNum):
    ticker = companyList.iloc[i]['Ticker']
    s = singleStock(ticker, 1, 1, 2008, 6, 28, 2016, 'm')
    isValid = s.loading()
    if isValid == 1:
        if s.Aclose.__len__()==102:
            stockData = tc.technicalCal(s)
            (xTrains, yTrains) = tc.featureExt(stockData)
            if np.isnan(xTrains).any() == False:
                if np.isinf(xTrains).any() == False:
                    validCompany.append(ticker)
validCompanyDf = pd.DataFrame(validCompany)
validCompanyDf.to_csv('./resources/SnP500_his.csv', index=False, header=False)

# myfile = open('./resources/SnP500_his.csv', 'wb')
# wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
# wr.writerow(validCompany)