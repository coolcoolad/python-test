# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import re
import time
import datetime
from stmpTool import sendEmail

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
	stocks = []
	with open('stocks.txt') as fd:
		for line in fd.readlines():
			line = line.decode('utf-8')
			stocks.append(line.strip().split(','))
	all = []
	for name, code in stocks:
		try:
			print name
			arr = getAnnouncement(code, name)
			all.extend(arr)
			if len(all) >= 10:
				now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				sendEmail("股票公告"+now, ('\n'.join(all)).encode('utf-8'))
				all = []
			time.sleep(144)
			# break
		except Exception, ex:
			print ex