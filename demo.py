import urllib2
import urllib
import cookielib
"""
response=urllib2.urlopen("http://www.baidu.com")
print response.read()
"""
"""
request=urllib2.Request("http://www.neu.edu.cn")
response=urllib2.urlopen(request)
print response.read()
"""
"""
values={"username":"waytoaccept@163.com","password":"v-shuphu6219"}
data=urllib.urlencode(values)
url="https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request=urllib2.Request(url,data)
response=urllib2.urlopen(request)
print response.read()
"""
"""
values={"username":"waytoaccept@163.com","password":"v-shuphu6219"}
data=urllib.urlencode(values)
url="https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
geturl=url+"?"+data
request=urllib2.Request(geturl,data)
response=urllib2.urlopen(request)
print response.read()
"""
"""
values={'username':'waytoaccept@163.com','password':'v-shuphu6219'}
url='https://passport.csdn.net/account/login?ref=toolbar'
user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
data=urllib.urlencode(values)
header={'User-Agent' : user_agent,'Referer':'https://passport.csdn.net/account/login?ref=toolbar'}
request=urllib2.Request(url,data,header)
response=urllib2.urlopen(request)
print response.read()
"""
"""
response=urllib2.urlopen("http://www.baidu.com",timeout=1)
print response.read()
"""
"""
httpHandler = urllib2.HTTPHandler(debuglevel=1)
httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
opener = urllib2.build_opener(httpHandler, httpsHandler)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.baidu.com')
print response.read()
"""
"""
request=urllib2.Request('http://www.xxx.com')
try:
	urllib2.urlopen(request)
except urllib2.URLError,e:
	print e.reson
"""
"""
req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.code
    print e.reason

"""
"""
#httpError is URLError child class
req = urllib2.Request('http://blog.csdn.net/cqcre')
try:
    urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.code
except urllib2.URLError, e:
    print e.reason
else:
	print 'OK'
"""
"""
#cookie
cookie=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
response=opener.open('http://www.baidu.com')
for item in cookie:
	print 'Name='+item.name
	print 'Value='+item.value

"""
"""
filename='cookie.txt'
cookie=cookielib.MozillaCookieJar(filename)
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)
response=opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)
"""

cookie=cookielib.MozillaCookieJar()
cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
req=urllib2.Request('http://www.baidu.com')
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
response=opener.open(req)
print response.read()