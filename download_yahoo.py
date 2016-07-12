import numpy as np
import csv
import requests

def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def is_date(m,d,y):
    if is_num(m) and is_num(d) and is_num(y):
        if 1<=m<=12 and 1<=d<=31 and y<=2016:
            return True
    return False

def spe_dat(s):
    if int(s)==8:
        return '08'
    if int(s)==9:
        return '09'
    return s

def form_url(ticker,m1,d1,y1,m2,d2,y2,freq):
    m1 = spe_dat(m1)
    m2 = spe_dat(m2)
    d1 = spe_dat(d1)
    d2 = spe_dat(d2)
    m1 = int(m1)
    m2 = int(m2)
    m1 -= 1
    m2 -= 1
    url =  'http://real-chart.finance.yahoo.com/table.csv?s='
    url += ticker + '&a=' + str(m1) + '&b=' + str(d1) + '&c=' + str(y1) + \
        '&d=' + str(m2) + '&e=' + str(d2) + '&f=' + str(y2) +'&g=' + \
        str(freq) +'&ignore=.csv'
    return url

class singleStock: 
    def __init__(self, ticker,m1,d1,y1,m2,d2,y2,freq):
        # grab data from m1/d1/y1 to m2/d2/y2 in the format of mm,dd,yyyy
        # freq = 'd','w','m' for daily,weekly and monthly data
        # verify the format of input
        if isinstance(ticker, basestring) and is_date(m1,d1,y1) and \
            is_date(m2,d2,y2) and 10000*y1+100*m1+d1<10000*y2+100*m2+d2:
            # make the url
            self.url = form_url(ticker,m1,d1,y1,m2,d2,y2,freq)
        else:
            print 'Error: check input'
            return
        self.ticker = ticker
        self.start_month = m1
        self.start_day = d1
        self.start_year = y1
        self.end_month = m2
        self.end_day = d2
        self.end_year = y2
        self.frequency = freq
        
    def loading(self):
        s = requests.Session()
        download = s.get(self.url)
        if download.status_code == 404:
            return 0
        decoded_content = download.content.decode('utf-8')
        ochl = csv.reader(decoded_content.splitlines(), delimiter=',')
    
        Date,Open,Close,High,Low,Aclose,Vol = [],[],[],[],[],[],[]
    
        for row in ochl:
            Date.append(row[0])
            Open.append(row[1])
            High.append(row[2])
            Low.append(row[3])
            Close.append(row[4])
            Vol.append(row[5])
            Aclose.append(row[6])
    
        self.Date = map(str,Date[1:])
        self.Open = map(float,Open[1:])
        self.High = map(float,High[1:])
        self.Low  = map(float,Low[1:])
        self.Close = map(float,Close[1:])
        self.Vol  = map(int,Vol[1:])
        self.Aclose = map(float,Aclose[1:])
        return 1
# example
#s = singleStock('aapl',3,9,2014,5,1,2015,'w')
#s.loading()
