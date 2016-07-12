from download_yahoo import singleStock
import csv


def monthlyLoad(startmonth, startyear, endmonth, endyear):
    with open('./resources/SnP500_his.csv', 'rb') as f:
        reader = csv.reader(f)
        ticker_list = list(reader)
    multiStockData = []
    for tickers in ticker_list:
        tickerstring = tickers[0]
        s = singleStock(tickerstring, startmonth, 1, startyear, endmonth, 1, endyear, 'm')
        s.loading()
        multiStockData.append(s)
    return multiStockData

