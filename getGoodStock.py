# -*- coding: utf-8 -*-
import pickle
import pandas as pd
from drawPriceProfitChat import saveReportData

def loadReportDataS4(startYear, endYear, basePath):
	return loadSeasonDataS4(startYear, endYear, basePath, 'report')

def loadSeasonDataS4(startYear, endYear, basePath, type):
	ans = None
	for year in range(startYear, endYear):
		season = 4
		try:
			suff = '.'.join(['', str(year), str(season), 'pickle'])
			path = basePath + type + suff
			with open(path, 'rb') as fd:
				df = pickle.load(fd)
				if len(df) > 0:
					if ans is None:
						ans = df
					else:
						ans = pd.concat([ans, df])
				else:
					print 'miss', type, year, season
		except Exception, ex:
			print ex
	return ans

if __name__ == '__main__':
	startYear = 2014
	endYear = 2017
	basePath = 'data/'

	with open('stocks.txt','w') as fd:
		# saveReportData(startYear, endYear, basePath)
		df = loadReportDataS4(startYear, endYear, basePath)
		codes = list(set(df['code']))
		for i, code in enumerate(codes):
				sub = df[df['code'] == code]
				tt = sub[sub['roe'] < 15]
				if len(tt) > 0:
					continue
				code, name = sub.iloc[0]['code'], sub.iloc[0]['name']
				fd.write((','.join([name,code])+'\n').encode('utf-8'))