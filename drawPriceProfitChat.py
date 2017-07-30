# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tushare as ts
import pickle
import pandas as pd
from datetime import date

def saveStockProfit(code, startYear, endYear, basePath):
    suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
    path = basePath + 'profit' + suff
    df = loadProfitData(code, startYear, endYear, basePath)
    df.to_pickle(path)

def saveStockReport(code, startYear, endYear, basePath):
    suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
    path = basePath + 'report' + suff
    df = loadProfitData(code, startYear, endYear, basePath)
    df.to_pickle(path)

def savePriceData(code, startYear, endYear, basePath):
    suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
    path = basePath+'price'+suff
    df = ts.get_h_data(code, start=str(startYear) + '-01-01', end=str(endYear) + '-01-01')
    df.to_pickle(path)

def loadPriceData(code, startYear, endYear, basePath):
    suff = '.'.join(['', code, str(startYear), str(endYear), 'pickle'])
    path = basePath+'price'+suff
    with open(path, 'rb') as fd:
        return pickle.load(fd)

def saveProfitData(startYear, endYear, basePath):
    for year in range(startYear, endYear):
        for season in range(1, 5):
            try:
                suff = '.'.join(['', str(year), str(season), 'pickle'])
                path = basePath+'profit'+suff
                df = ts.get_profit_data(year, season)
                df.to_pickle(path)
            except Exception, ex:
                print ex

def saveReportData(startYear, endYear, basePath):
    for year in range(startYear, endYear):
        for season in range(1, 5):
            try:
                suff = '.'.join(['', str(year), str(season), 'pickle'])
                path = basePath+'report'+suff
                df = ts.get_report_data(year, season)
                df.to_pickle(path)
            except Exception, ex:
                print ex

def loadProfitData(code, startYear, endYear, basePath):
    ans = None
    for year in range(startYear, endYear):
        for season in range(1, 5):
            try:
                suff = '.'.join(['', str(year), str(season), 'pickle'])
                path = basePath + 'profit' + suff
                with open(path, 'rb') as fd:
                    df = pickle.load(fd)
                    row = df.loc[df['code'] == code]
                    m = len(row['code'])
                    if m == 1:
                        row = row.assign(date=[date(year, ((season)*3+2)%12, 15)])
                    if ans is None:
                        ans = row
                    else:
                        ans = pd.concat([ans, row])
            except Exception, ex:
                print ex
    ans = ans.set_index(pd.DatetimeIndex(ans['date']))
    return ans

if __name__ == '__main__':
    startYear = 2017
    endYear = 2018
    basePath = 'data/'

    # saveProfitData(startYear, endYear, basePath)
    saveReportData(startYear, endYear, basePath)

    # code = '300027'
    # saveStockProfit(code, startYear, endYear, basePath)
    # savePriceData(code, startYear, endYear, basePath)
    #
    # code = '300027'
    # priceDf = loadPriceData(code, startYear, endYear, basePath)['close']
    # profitDf = loadProfitData(code, startYear, endYear, basePath)
    # fig, axis = plt.subplots(4, 1)
    # priceDf.plot(ax=axis[0])
    # profitDf['roe'].plot(ax=axis[1], kind='bar')
    # profitDf['net_profit_ratio'].plot(ax=axis[2], kind='bar')
    # profitDf['gross_profit_rate'].plot(ax=axis[3], kind='bar')
    # plt.show()