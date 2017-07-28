# -*- coding: utf-8 -*-

import tushare as ts
import json

def main():
	# df =  ts.get_profit_data(2000, 1)
	# print type(df['name'][0]), type(df['roe'][0]), type(df['net_profits'][0])
	# return
	names = ['code', 'name', 'roe', 'net_profit_ratio', 'gross_profit_rate', 'net_profits', 'eps', 'business_income', 'bips']
	#names = ['code', 'name', 'time', 'price', 'volume', 'preprice', 'type']
	for offset in range(20):
		for season in range(1,5):
			jsonMap = {'colNames': names, 'rows':[]}
			base = 2000
			year = base+offset
			try:
			# df = ts.get_sina_dd('600816', date=yearStr+'-7-20', vol=1000)
				df = ts.get_profit_data(year, season)
				if df is None:
					continue
			except Exception, ex:
				print ex
				continue
			m = len(df[names[0]])
			for i in range(m):
				map_ = {}
				for name in names:
					if type(df[name][i]) == str:
						map_[name] = df[name][i]
					elif type(df[name][i]) == unicode:
						map_[name] = df[name][i].encode('utf-8')
					else:
						try:
							map_[name] = float(df[name][i])
						except Exception, ex:
							print ex
							map_[name] = 'NaN'
				jsonMap['rows'].append(map_)
			with open('profitData/'+('.'.join(['profit',str(year),str(season),'json'])),'w') as fd:
				json.dump(jsonMap, fd, encoding='utf-8', indent=4, separators=[',', ':'], ensure_ascii=False)
				#return

if __name__ == '__main__':
	main()