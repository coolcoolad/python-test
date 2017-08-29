# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import pickle
import pandas as pd
from datetime import date
import matplotlib.dates as mdate
import os
import numpy

# def saveStockProfit(code, startYear, endYear, basePath):
# 	suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
# 	path = basePath + 'profit' + suff
# 	df = loadProfitData(code, startYear, endYear, basePath)
# 	df.to_pickle(path)
#
#
# def saveStockReport(code, startYear, endYear, basePath):
# 	suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
# 	path = basePath + 'report' + suff
# 	df = loadProfitData(code, startYear, endYear, basePath)
# 	df.to_pickle(path)

def saveBasicData(basePath):
	suff = '.'.join(['','pickle'])
	path = basePath + 'basic' + suff
	df = ts.get_stock_basics()
	df.to_pickle(path)

def loadBasicData(code, basePath):
	suff = '.'.join(['','pickle'])
	path = basePath + 'basic' + suff
	with open(path, 'rb') as fd:
		df = pickle.load(fd)
		return df.loc[code]

def savePriceData(code, startYear, endYear, basePath):
	suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
	path = basePath + 'price' + suff
	# if os.path.isfile(path):
	# 	return
	df = ts.get_h_data(code, start=str(startYear) + '-01-01', end=str(endYear) + '-01-01')
	df.to_pickle(path)


def loadPriceData(code, startYear, endYear, basePath):
	suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
	path = basePath + 'price' + suff
	with open(path, 'rb') as fd:
		return pickle.load(fd)


def saveProfitData(startYear, endYear, basePath):
	for year in range(startYear, endYear):
		for season in range(1, 5):
			try:
				suff = '.'.join(['', str(year), str(season), 'pickle'])
				path = basePath + 'profit' + suff
				df = ts.get_profit_data(year, season)
				df.to_pickle(path)
			except Exception, ex:
				print ex


def saveReportData(startYear, endYear, basePath):
	for year in range(startYear, endYear):
		for season in range(1, 5):
			try:
				suff = '.'.join(['', str(year), str(season), 'pickle'])
				path = basePath + 'report' + suff
				df = ts.get_report_data(year, season)
				# print df.loc[df['code'] == '000651']
				df.to_pickle(path)
			except Exception, ex:
				print ex


def loadProfitData(code, startYear, endYear, basePath):
	return loadSeasonData(code, startYear, endYear, basePath, 'profit')

def loadReportData(code, startYear, endYear, basePath):
	return loadSeasonData(code, startYear, endYear, basePath, 'report')

def loadSeasonData(code, startYear, endYear, basePath, type):
	ans = None
	for year in range(startYear, endYear):
		for season in range(1, 5):
			try:
				suff = '.'.join(['', str(year), str(season), 'pickle'])
				path = basePath + type + suff
				with open(path, 'rb') as fd:
					df = pickle.load(fd)
					path = basePath + 'report' + suff
					with open(path, 'rb') as reportFd:
						reportDf = pickle.load(reportFd)
						row = df.loc[df['code'] == code]
						reportRow = reportDf.loc[reportDf['code'] == code]
						m = len(row)
						if m > 0:
							row = row.iloc[0:1]
							n = len(reportRow)
							row = row.assign(date=date(year if season < 4 else year+1, season * 3+2 if season < 4 else 2, 20))
							flag = True
							if n > 0:
								reportRow = reportRow.iloc[0:1]
								reportDate = reportRow.iloc[0]['report_date']
								if reportDate != '':
									tArr = reportDate.split('-')
									month = int(tArr[0])
									day = int(tArr[1])
									row = row.assign(date=date(year if season < 4 else year+1, month, day))
									flag = False
							if flag:
								print 'mock', type, code, year, season
							if ans is None:
								ans = row
							else:
								ans = pd.concat([ans, row])
						else:
							print 'miss', type, code, year, season
			except Exception, ex:
				print ex
	ans = ans.set_index(pd.DatetimeIndex(ans['date']))
	ans.duplicated('date')
	ans = ans[~ans.index.duplicated('last')]
	return ans


if __name__ == '__main__':
	startYear = 2014
	endYear = 2018
	basePath = 'data/'
	code = '000651'

	# saveBasicData(basePath)
	# saveReportData(startYear, endYear, basePath)
	# savePriceData(code, startYear, endYear, basePath)
	# saveProfitData(startYear, endYear, basePath)
	basic = loadBasicData(code, basePath)
	totals = basic['totals']
	priceSer = loadPriceData(code, startYear, endYear, basePath)['close']
	priceSer = priceSer.sort_index()
	profitDf = loadProfitData(code, startYear, endYear, basePath)
	reportDf = loadReportData(code, startYear, endYear, basePath)
	netSer = profitDf['net_profits']
	bvpsSer = reportDf['bvps']
	#计算每期扣非净利润
	col = []
	for i in range(len(netSer)-1, 0, -1):
		if netSer[i] > netSer[i-1]:
			col.append(netSer[i] - netSer[i - 1])
		else:
			col.append(netSer[i])
	col.append(netSer[0])
	col.reverse()
	i = 0
	for index, val in netSer.iteritems():
		netSer.set_value(index, col[i])
		i += 1
	#计算pe
	peSer = pd.Series()
	netDates = netSer.index
	priceDates = priceSer.index
	i = 0
	j = 0
	while priceDates[j] < netDates[i]:
		j += 1
	i += 1
	while i < len(netDates):
		while j < len(priceDates) and priceDates[j] < netDates[i]:
			net = netSer[netDates[i-1]]
			# if type(net) != numpy.float64:
			# 	net = net.iloc[0]
			pe = priceSer[priceDates[j]] / net * totals * 25
			peSer.set_value(priceDates[j], pe)
			j += 1
		i += 1
	while j < len(priceDates):
		net = netSer[netDates[i-1]]
		# if type(net) != numpy.float64:
		# 	net = net.iloc[0]
		pe = priceSer[priceDates[j]] / net * totals * 25
		peSer.set_value(priceDates[j], pe)
		j += 1
	#计算pb
	pbSer = pd.Series()
	bvpsDates = bvpsSer.index
	i = 0
	j = 0
	while priceDates[j] < bvpsDates[i]:
		j += 1
	i += 1
	while i < len(bvpsDates):
		while j < len(priceDates) and priceDates[j] < bvpsDates[i]:
			pbSer.set_value(priceDates[j], priceSer[priceDates[j]] / bvpsSer[bvpsDates[i-1]])
			j += 1
		i += 1
	while j < len(priceDates):
		pbSer.set_value(priceDates[j], priceSer[priceDates[j]] / bvpsSer[bvpsDates[i-1]])
		j += 1
	#计算roe
	roeSer = pd.Series()
	i = 0
	if len(bvpsDates) < len(netDates):
		dates = bvpsDates
	while i < len(dates):
		roeSer.set_value(dates[i], netSer[dates[i]] / (bvpsSer[dates[i]] * totals) * 4)
		i += 1
	fig, axis = plt.subplots(3, 1)
	plt.ion()
	ax = priceSer.plot(ax=axis[0], grid=True)
	ax.set_xlim(pd.Timestamp(str(startYear)+'-01-01'), pd.Timestamp(str(endYear)+'-01-01'))
	ax = netSer.plot(ax=axis[1], grid=True)
	ax.set_xlim(pd.Timestamp(str(startYear)+'-01-01'), pd.Timestamp(str(endYear)+'-01-01'))
	ax = peSer.plot(ax=axis[2], grid=True)
	ax.set_xlim(pd.Timestamp(str(startYear)+'-01-01'), pd.Timestamp(str(endYear)+'-01-01'))
	# ax = pbSer.plot(ax=axis[3], grid=True)
	# ax.set_xlim(pd.Timestamp(str(startYear)+'-01-01'), pd.Timestamp(str(endYear)+'-01-01'))
	# ax = roeSer.plot(ax=axis[4], grid=True)
	# ax.set_xlim(pd.Timestamp(str(startYear)+'-01-01'), pd.Timestamp(str(endYear)+'-01-01'))
	plt.show()

	fig = plt.figure()
	axis = fig.add_subplot(221)
	roeSer.plot(ax=axis, kind='bar', grid=True)
	axis = fig.add_subplot(222)
	netSer.plot(ax=axis, kind='bar', grid=True)
	axis = fig.add_subplot(223)
	pbSer.plot(ax=axis, grid=True)
	plt.show()
	plt.pause(1000)

	# savePriceData(code, startYear, endYear, basePath)
	# priceDf = loadPriceData(code, startYear, endYear, basePath)['close']
	# reportDf = loadReportData(code, startYear, endYear, basePath)
	# fig, axis = plt.subplots(5, 1)
	# priceDf.plot(ax=axis[0])
	# reportDf['roe'].plot(ax=axis[1], kind='bar')
	# reportDf['eps'].plot(ax=axis[2], kind='bar')
	# reportDf['bvps'].plot(ax=axis[3], kind='bar')
	# reportDf['epcf'].plot(ax=axis[4], kind='bar')
	# plt.show()

	# saveReportData(startYear, endYear, basePath)

	# savePriceData(code, startYear, endYear, basePath)

	# priceDf = loadPriceData(code, startYear, endYear, basePath)['close']
	# profitDf = loadProfitData(code, startYear, endYear, basePath)
	# fig, axis = plt.subplots(5, 1)
	# priceDf.plot(ax=axis[0])
	# profitDf['roe'].plot(ax=axis[1], kind='bar')
	# profitDf['net_profit_ratio'].plot(ax=axis[2], kind='bar')
	# profitDf['gross_profit_rate'].plot(ax=axis[3], kind='bar')
	# profitDf['business_income'].plot(ax=axis[4], kind='bar')
	# plt.show()

	# priceDf = loadPriceData(code, startYear, endYear, basePath)['close']
	# reportDf = loadReportData(code, startYear, endYear, basePath)
	# fig, axis = plt.subplots(5, 1)
	# priceDf.plot(ax=axis[0])
	# reportDf['roe'].plot(ax=axis[1], kind='bar')
	# reportDf['eps'].plot(ax=axis[2], kind='bar')
	# reportDf['bvps'].plot(ax=axis[3], kind='bar')
	# reportDf['epcf'].plot(ax=axis[4], kind='bar')
	# plt.show()
