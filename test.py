import tushare as ts
import datetime
import pandas as pd
import matplotlib.pyplot as plt
# date = datetime.date(2017,7,1)
# delta = datetime.timedelta(days=1)
# sum = 0
# for i in range(60):
# 	try:
# 		df = ts.day_boxoffice(date.strftime('%Y-%m-%d'))
# 		print df['BoxOffice'].iloc[0], df['MovieName'].iloc[0]
# 		sum += float(df['BoxOffice'].iloc[0])
# 		date = date+delta
# 	except:
# 		pass
# print sum
# print ts.realtime_boxoffice()
# print ts.day_boxoffice('2016-6-5')
# df = ts.get_report_data(2017, 1)
# print df.loc[df['code'] == '000651']
# ser = pd.Series()
# ser.set_value(datetime.date(2016,1,1), 1000)
# ser.plot(kind='bar')
# plt.show()
# df = ts.forecast_data(2017, 2)
# print df[df['code'] == '000792']
print ts.profit_data(top=60)
