# -*- coding: utf-8 -*-

import urllib2
import sys

def main(url):
	req = urllib2.Request(url)
	req.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
	response = urllib2.urlopen(req)
	data = response.read()
	with open(url+'.v', 'wb') as fd:
		fd.write(data)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "cmd url"
	else:
		url = sys.argv[1]
		main(url)
