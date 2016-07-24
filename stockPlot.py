from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.dates import DateFormatter, WeekdayLocator, \
    DayLocator, MONDAY
import matplotlib.pyplot as plt
from download_yahoo import singleStock
import matplotlib.dates as md
from datetime import datetime
import numpy as np
def spyBenchPlot(m1, d1, y1, m2, d2, y2):
    """
    plot the s%p 500 index(ticker: spy) candlestick chart
    :param m1: staring month
    :param d1: starting day
    :param y1: starting year
    :param m2: ending month
    :param d2: ending day
    :param y2: ending year
    :return:
    """
    date1 = (y1, m1, d1)
    date2 = (y2, m2, d2)
    mondays = WeekdayLocator(MONDAY)  # major ticks on the mondays
    alldays = DayLocator()  # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12

    quotes = quotes_historical_yahoo_ohlc('spy', date1, date2)
    if len(quotes) == 0:
        raise SystemExit

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    candlestick_ohlc(ax, quotes, width=0.6)
    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.title('S&P 500 ETF')
    plt.show()

def singleTradePlot_pctc(dates, real_pctc, pred_pctc):
    """
    plot the real and predicted percentage change of stock price
    :param dates: date list from singleStock class
    :param real_pctc: 1-D array, real percentage change
    :param pred_pctc: 1-D array, predicted percentage change
    :return:
    """
    date_dt = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
    date_plt = md.date2num(date_dt)
    data_format = md.DateFormatter('%Y-%m-%d')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.patch.set_facecolor('lightgrey')
    ax.xaxis.set_major_formatter(data_format)
    ax.set_xlabel('date')
    ax.set_ylabel('Percentage change')
    plt.setp(ax.get_xticklabels(), size=8)
    ax.plot(date_plt, real_pctc, label="Real Pct Change", linewidth=2)
    ax.plot(date_plt, pred_pctc, label="Predicted Pct Change", linewidth=2)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.grid()
    plt.show()

def correctRate(ticker,m1,d1,y1,m2,d2,y2,freq, ochl, pred):
    """
    calculate the rate of correction for a binary predictions.
    :param ticker:
    :param m1: staring month
    :param d1: starting day
    :param y1: starting year
    :param m2: ending month
    :param d2: ending day
    :param y2: ending year
    :param freq: sampling frequency: 'd' for day, 'w' for week and 'm' for month
    :param ochl: price type: 'o' for opening, 'c' for closing, 'h' for high and 'l' for low
    :param pred: list of prediction results. Positive number stands for price increase,
                negative number for price dropping
    :return: the rate of correction
    """
    length = len(pred)
    pred_change = np.array(pred)
    s = singleStock(ticker,m1,d1,y1,m2,d2,y2,freq)
    s.loading()
    if ochl == 'o':
        price_array = s.Open
        price_array1 = np.array(s.Open)
        price_array.pop(0)
        price_array.append(0)
        diff_array = price_array1 - np.array(price_array)
        real_change = np.delete(diff_array, length-1)
        product = pred_change * real_change
        correct_num = (product > 0).sum()
        rate = float(correct_num)/length
    if ochl == 'c':
        price_array = s.Close
        price_array1 = np.array(s.Close)
        price_array.pop(0)
        price_array.append(0)
        diff_array = price_array1 - np.array(price_array)
        real_change = np.delete(diff_array, length-1)
        product = pred_change * real_change
        correct_num = (product > 0).sum()
        rate = float(correct_num)/length
    if ochl == 'h':
        price_array = s.High
        price_array1 = np.array(s.High)
        price_array.pop(0)
        price_array.append(0)
        diff_array = price_array1 - np.array(price_array)
        real_change = np.delete(diff_array, length-1)
        product = pred_change * real_change
        correct_num = (product > 0).sum()
        rate = float(correct_num)/length
    if ochl == 'l':
        price_array = s.Low
        price_array1 = np.array(s.Low)
        price_array.pop(0)
        price_array.append(0)
        diff_array = price_array1 - np.array(price_array)
        real_change = np.delete(diff_array, length-1)
        product = pred_change * real_change
        correct_num = (product > 0).sum()
        rate = float(correct_num)/length

    return rate

def portfolioVSspy(m1,y1,m2,y2, pred):
    # calculate the percentage change of s&p 500 index
    s = singleStock('spy', m1, 1, y1, m2, 28, y2, 'm')
    s.loading()
    price_array = s.Aclose
    pct_change_plt = np.zeros(len(price_array)-1)
    for i in range(1, len(price_array)):
        pct_change_plt[i-1] = (price_array[i] - price_array[i-1])/price_array[i-1]
    pct_change_plt = np.array(pct_change_plt)
    maxY = max(max(pct_change_plt), max(pred))
    minY = min(min(pct_change_plt), min(pred))
    date_dt = [datetime.strptime(d, '%Y-%m-%d') for d in s.Date]
    date_plt = md.date2num(date_dt)
    date_plt = np.delete(date_plt,0,0)
    data_format = md.DateFormatter('%Y-%m-%d')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.patch.set_facecolor('lightgrey')
    ax.xaxis.set_major_formatter(data_format)
    ax.set_xlabel('date')
    ax.set_ylabel('Percentage change')
    plt.setp(ax.get_xticklabels(), size=8)
    plt.ylim([2*minY,2*maxY])
    ax.plot(date_plt, pct_change_plt, label="S&P benchmark", linewidth=2)
    ax.plot(date_plt, pred, label="portfolio", linewidth=2)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.)
    plt.grid()
    plt.show()