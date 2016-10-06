# -*- coding: utf-8 -*-
import os
import sys
import urllib
import urllib2
import re
import thread
import time
import codecs

class CSDN:

	def __init__(self):
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
		self.headers = {'User-Agent': self.user_agent}
		# 存放程序是否继续运行的变量
		self.rootURL='http://blog.csdn.net'
		self.rootPATH='E:/Python_Spider'
		self.enable = False

	# 传入某一页的索引获得页面代码
	def getArticleList(self,user, pageIndex):
		try:
			url = self.rootURL+'/' +user+'/article/list/'+ str(pageIndex)
			print url
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			pageCode = response.read().decode('utf-8')
			#print pageCode
			if not pageCode:
				return None
			pattern=re.compile('class="pagelist">.*?<span>\s(\d+).*?</span>',re.S)
			item=re.findall(pattern,pageCode)
			totalArticles=item[0]
			pattern=re.compile('link_title"><a href="(.*?)">(.*?)</a>',re.S)
			items=re.findall(pattern,pageCode)
			articleList=[]
			for item in items:
				articleList.append([self.rootURL+item[0].strip(),item[1].strip()])
				print self.rootURL+item[0]+'-----'+item[1].strip()
			return (articleList,totalArticles)
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"连接CSDN，错误原因", e.reason
				return None
	#请求文章链接
	def getArticle(self,user,articleList,totalArticles):
		num=0
		if articleList:
			for item in articleList:
				#print item,item[0],item[1]
				try:
					num+=1
					request=urllib2.Request(item[0],headers=self.headers)
					response=urllib2.urlopen(request)
					pageCode = response.read().decode('utf-8')
					if not pageCode:
						print u'链接无效'
						return None
					title=item[1]
					pattern=re.compile('details/(\d+)',re.S)
					articleID=re.findall(pattern,item[0])
					pattern=re.compile('class="article_content">(.*?)</div>',re.S)
					text=re.findall(pattern,pageCode)
					article=text[0]
					#修复代码块
					article=self.repairCode(article)
					#保存文件
					self.save(user,articleID,title,article)
					#time.sleep(2)
				except urllib2.URLError,e:
					if hasattr(e,"reason"):
						print u"连接CSDN，错误原因", e.reason
						return None
			return num
	#保存文件
	def save(self,user,articleID,title,article):
		try:
			path=self.rootPATH+'/'+'BlogCSDN'+'/'+user
			#path=self.rootPATH+'//'+user
			#print path
			if not os.path.exists(path):
				os.makedirs(path)
			fileName=title+'---'+articleID[0]+'.txt'
			fileName=path+'/'+fileName
			if os.path.exists(fileName):
				print u'%s 文件已经存在' % (fileName)
				return None
			fobj =codecs.open(fileName, 'w','utf-8')
			fobj.write(title+'\n'+article)
			fobj.close()
		except IOError,e:
			print e.reason
			return None
	#去掉标签，替换特殊字符
	def repairCode(self,text):
		#去除标签
		replace = re.compile('</\w+>')
		text = re.sub(replace,"\r\n",text)
		replace = re.compile('<.*?>')
		text = re.sub(replace,"",text)
		rTermsDict={'&lt;':'<','&gt;':'>','&amp;':'&','&quot;':'"','&nbsp;':' '}
		for item in rTermsDict.keys():
			replace = re.compile(item)
			text = re.sub(replace,rTermsDict[item],text)
		#if codeType!='cpp':
			#扩展不同的代码
			#return text
		#对齐代码块
		return text
	#代码写的好乱
	def start(self):
		#想继续扩展成多线程
		user="waytoaccept"
		print "reading "+user+"'s blog"
		self.enable = True
		pageIndex=1;
		num=0
		while (self.enable):
			print 'reading page:'+str(pageIndex)+' list'
			(articleList,total)=self.getArticleList(user,pageIndex)
			if total==None:
				print u'获取文章失败!'
				break
			articleNum=int(total)
			if articleList and num<articleNum:
				num+=self.getArticle(user,articleList,articleNum)
				print u'共 %d 篇博客,已下载 %d 篇\n' % (articleNum,num)
				if num>=articleNum:
					print u'用户%s的博客已经下载完毕！' % (user)
					self.enable=False
					continue
				print u'是否继续下载，任意键继续，Q退出'
				input=raw_input()
				if input=='Q':
					self.enable=False
				else:
					pageIndex+=1
			else:
				break
		print u'欢迎下次使用CSDN爬虫！'
spider = CSDN()
spider.start()


