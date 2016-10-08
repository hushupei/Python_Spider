# -*- coding: utf-8 -*-
import os
import sys
import urllib
import urllib2
import re
import thread
import time
import codecs
import threading
class USER:
	def __init__(self,userName,path):
		self.name=userName
		self.articleList=[]
		self.articleNum=0
		self.pageIndex=1
		self.rootURL='http://blog.csdn.net'
		self.contentURL='http://blog.csdn.net/'+self.name+'/article/list/'+str(self.pageIndex)
		self.rootPath=path+'/BlogCSDN/'+self.name
	def openURL(self,url):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
		try:
			request = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8')
			return pageCode
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接CSDN，错误原因", e.reason
				return None
	def getList(self):
		try:
			url = self.rootURL+'/' +self.name+'/article/list/'+ str(self.pageIndex)
			if self.articleNum==0:
				pageCode=self.openURL(url)
				if pageCode!=None:
					#正则表达式当有多个括号时，返回为字符串元祖列表[(),(),...()]
					#每一个元组元素包含的字符串数与表达式中的括号一致
					#比如下式返回值可能为[('20','18','3')]
					#正则表达式有1个或0个括号时，返回值为字符串列表['aaaa','ddd']
					pattern=re.compile('blog_statistics">.*?<span>(\d+).*?</span>.*?<span>(\d+).*?</span>.*?<span>(\d+).*?</span>',re.S)
					items=re.findall(pattern,pageCode)
					for m in items[0]:
						self.articleNum+=int(m)
			num=0
			articleList=[]
			while num<self.articleNum:
				url = self.rootURL+'/' +self.name+'/article/list/'+ str(self.pageIndex)
				pageCode=self.openURL(url)
				if not pageCode:
					return None
				pattern=re.compile('link_title"><a href="(.*?)">(.*?)</a>',re.S)
				items=re.findall(pattern,pageCode)
				for item in items:
					articleList.append([self.rootURL+item[0].strip(),item[1].strip()])
					#print self.rootURL+item[0]+'-----'+item[1].strip()
					num+=1
					if num>=self.articleNum:
						break
				self.pageIndex+=1
			self.articleList=articleList
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接CSDN，错误原因", e.reason
				return None
	def getArticle(self):
		for item in self.articleList:
			pageCode=self.openURL(item[0])
			if not pageCode:
				print u'链接无效'
				return None
			pattern=re.compile('class="article_content">(.*?)</div>',re.S)
			content=re.findall(pattern,pageCode)
			articleID=(item[0].split('/'))[6]
			title=item[1]
			fileName=self.rootPath+'/'+title+'---'+articleID+'.txt'
			#这个地方刚开始少写了'[0]'，造成编码对不上，花费了许多时间
			text=content[0]
			text=self.repairCode(text)
			self.saveArticle(fileName,text)
			print self.name+':'+articleID+'.txt has saved!'
	def saveArticle(self,fileName,text):
		if not os.path.exists(self.rootPath):
			os.makedirs(self.rootPath)
		try:
			if os.path.exists(fileName):
				print u'%s 文件已经存在' % (fileName)
				return None
			fobj =codecs.open(fileName, 'w+','utf-8')
			fobj.write(text)
			fobj.close()
		except IOError:
			print 'IO error!'
			return None
	def repairCode(self,text):
		#去除标签
		replace = re.compile('</\w+>')
		text = re.sub(replace,"\r\n",text)
		replace = re.compile('<.*?>')
		text = re.sub(replace,"",text)
		rTermsDict={'&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"','&nbsp;':' ','&#39;':'\'','&#43;':'+'}
		for item in rTermsDict.keys():
			replace = re.compile(item)
			text = re.sub(replace,rTermsDict[item],text)
		#if codeType!='cpp':
			#扩展不同的代码
			#return text
		#对齐代码块
		return text
	def start(self):
		print 'reading %s blog...' % (self.name)
		self.getList()
		self.getArticle()
		print "%s  blog %d has saved!" % (self.name,self.articleNum)

class CSDNSPIDER:

	def __init__(self):
		# 存放程序是否继续运行的变量
		self.rootPATH='E:/Python_Spider'
		self.enable = False
	def start(self):
		#想继续扩展成多线程
		userList=['waytoaccept','xiaosebi1111','zhiyuan_2007']
		thrList=[]
		for name in userList:
			user=USER(name,self.rootPATH)
			t=threading.Thread(target=user.start,name=name)
			thrList.append(t)
		for thr in thrList:
			thr.start()
		for thr in thrList:
			thr.join()
		self.enable = True
		print u'欢迎下次使用CSDN爬虫！'
spider = CSDNSPIDER()
spider.start()


