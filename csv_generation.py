import pandas as pd

df = pd.read_csv('./resources/SnP500.csv', usecols=['Ticker symbol'])
print df.head(5)
df.to_csv('./resources/SnP500_tickers.csv', index=False, header=False)
