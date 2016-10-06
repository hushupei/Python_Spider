import re
strlist='this is list'
pattern=re.compile('me',re.S)
text=re.findall(pattern,strlist)
print text
tulist=('this is a tupe',)
dictm={'1a':'<','2b':'>'}
"""
print strlist[0]
print tulist[0]
for item in dictm.keys():
	print item,dictm[item]
"""