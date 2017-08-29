# -*- coding: utf-8 -*-
import pickle
import pandas as pd
from drawPriceProfitChat import saveReportData
import urllib
from bs4 import BeautifulSoup
import re
import time
import datetime
from stmpTool import sendEmail

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

def getAnnouncement(code, name):
	url = 'http://search.10jqka.com.cn/search?preParams=&ts=1&f=1&qs=site_stockpage_more&querytype=&tid=pubnote&bgid=&sdate=&edate=&tid=pubnote&w='+code
	resp = urllib.urlopen(url)
	content = resp.read()
	soup = BeautifulSoup(content,'lxml')
	# print soup.prettify()
	divs = soup.find_all(class_='s_r_box')
	map = {}
	ans = []
	for div in divs:
		arr = div.find_all(text=re.compile(u'度报告|实施|分派|分红|送股|送转股'))
		if len(arr) > 0:
			title = arr[0]
			time = div.find(text=re.compile(u'月')).strip()
			time = time[:time.find(u'日')+1]
			date = datetime.datetime.strptime(time.encode('utf-8'), '%Y年%m月%d日').date()
			today = datetime.date.today()
			if date >= today:
				map[time] = title
	for k, v in map.items():
		ans.append(','.join([name, code, k, v]))
	return ans

if __name__ == '__main__':
	startYear = 2014
	endYear = 2017
	basePath = 'data/'
	code = '000651'

	# saveReportData(startYear, endYear, basePath)
	df = loadReportDataS4(startYear, endYear, basePath)
	codes = list(set(df['code']))
	all = []
	for i, code in enumerate(codes):
		sub = df[df['code'] == code]
		tt = sub[sub['roe'] < 15]
		if len(tt) > 0:
			continue
		code, name = sub.iloc[0]['code'], sub.iloc[0]['name']
		print name
		arr = getAnnouncement(code, name)
		all.extend(arr)
		if len(all) >= 10:
			now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			sendEmail("股票公告"+now, ('\n'.join(all)).encode('utf-8'))
			all = []
		time.sleep(144)
		# break