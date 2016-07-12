import pandas as pd
import technicals

def technicalCal(stockData):
    dic = {'date': stockData.Date, 'Open': stockData.Open, 'Close': stockData.Close, 'High': stockData.High,
           'Low': stockData.Low, 'Volume': stockData.Vol}
    df = pd.DataFrame(data=dic)
    df = technicals.MA(df, 9)
    df = technicals.EMA(df, 9)
    df = technicals.MOM(df, 9)
    df = technicals.ROC(df, 9)
    df = technicals.ATR(df, 9)
    df = technicals.BBANDS(df, 9)
    df = technicals.PPSR(df)
    df = technicals.STOK(df)
    df = technicals.STO(df, 9)
    df = technicals.TRIX(df, 9)
    df = technicals.MassI(df)
    df = technicals.Vortex(df, 9)
    df = technicals.RSI(df, 9)
    df = technicals.ACCDIST(df, 9)
    df = technicals.Chaikin(df)
    df = technicals.MFI(df, 9)
    df = technicals.OBV(df, 9)
    df = technicals.FORCE(df, 9)
    df = technicals.EOM(df, 9)
    df = technicals.CCI(df, 9)
    df = technicals.COPP(df, 9)
    df = technicals.DONCH(df, 9)
    df = technicals.STDDEV(df, 9)


    return df
