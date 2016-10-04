# -*- coding: utf-8 -*-
import os
import urllib
import urllib2
import re
import thread
import time

class IEEE:

	def __init__(self):
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
		self.headers = {'User-Agent': self.user_agent}
		# 存放程序是否继续运行的变量
		self.enable = False

	# 传入某一页的索引获得页面代码
	def getPage(self):
		try:
			url = 'http://ieeexplore.ieee.org/ielx7/9739/7548084/07548121.pdf?tp=&arnumber=7548121&isnumber=7548084'
			time.sleep(10)
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			"""
			file_name="test.pdf"
			f = open(file_name, 'wb')
			bufferLen = 8192
			while True:
				buffer = response.read(bufferLen)
				if not buffer:
					break
			f.write(buffer)
			f.close()
			"""
			content=response.read()
			response.close()
			print "success download:\n"+content
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"error reason：", e.reason
				return None

	
	def start(self):
		print "reading"
		self.enable = True
		self.getPage()

spider = IEEE()
spider.start()


