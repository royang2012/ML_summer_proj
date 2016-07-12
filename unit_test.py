import stock_load as sl
import technical_cal
import pandas as pd
multiStock = sl.monthlyLoad(1, 2013, 1, 2015)
test0 = technical_cal.technicalCal(multiStock[0])
print test0

