# -*- coding: utf-8 -*-

# XSHG 上海证券交易所
# XSHE 深圳证券交易所

# 每股收益eps必须按年取，数据才对fundamentals.financial_indicator.earnings_per_share

# roe
code = '600816.XSHG'
indicator = fundamentals.financial_indicator
dataTypes = [indicator.return_on_equity_weighted_average
	# indicator.return_on_equity,
	# indicator.return_on_equity_weighted_average,
	# indicator.return_on_equity_diluted,
	# indicator.adjusted_return_on_equity_average,
	# indicator.adjusted_return_on_equity_weighted_average,
	# indicator.adjusted_return_on_equity_diluted
]
dp = get_fundamentals(query(*dataTypes).filter(fundamentals.stockcode == code), '2017-08-02', '10y').minor_xs(code)
logger.info(dp)
put_file(code+'.roe.csv', dp.to_csv())

# 基本表
def saveCodeBasic(code, time, seasonNum, prefix='ord'):
  indicator = fundamentals.eod_derivative_indicator
  dataTypes = [indicator.pe_ratio, fundamentals.financial_indicator.adjusted_net_profit]
  dp = get_fundamentals(query(*dataTypes).filter(fundamentals.stockcode == code), time, seasonNum).minor_xs(code)
  logger.info(dp)
  #put_file('.'.join([prefix, code,'pe','net','csv']), dp.to_csv())
  return dp

dp = saveCodeBasic('300027.XSHE','2017-7-1','40q')
# plot('pe', dp['pe_ratio'])
# plot('net', dp['adjusted_net_profit'])

# roe filter
indicator = fundamentals.financial_indicator
dataTypes = [indicator.return_on_equity_weighted_average] #adjusted_return_on_equity_diluted
num = 12
dp = get_fundamentals(query(*dataTypes), '2017-7-1', str(num) + 'q') #只返回季度数据
dp = dp.iloc[0].T
cols = dp.columns
limit = 6
dp = dp[lambda dp: sum([dp[cols[i]] > limit for i in range(num)]) == num]
logger.info(dp)
put_file('.'.join([str(num), str(limit), 'roe.csv']), dp.to_csv())
codes = dp.index
for code in codes:
    logger.info(instruments(code))
    saveCodeBasic(code, '2017-7-1', '20d', 'good')
