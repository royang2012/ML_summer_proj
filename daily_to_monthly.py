import pandas as pd

dfrm = pd.read_csv('./resources/daily4.lcsv.csv', usecols=['date', 'TICKER', 'PRC'], parse_dates=True)
dfrm['date'] = pd.to_datetime(dfrm['date'], format='%Y%m%d')
normalized = dfrm.pivot_table(index='date', columns='TICKER', values='PRC')
normalized['date'] = normalized.index

print normalized.head(5)

monthlyDF = normalized.groupby(by=normalized.date.map(lambda x: (x.year, x.month))). \
    apply(lambda x: x.sort_values(by='date', ascending=True).head(1))

print monthlyDF.head(5)

monthlyDF.to_csv('./resources/monthly_2011_2015.csv')
