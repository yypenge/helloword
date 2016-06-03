#-*- coding:utf-8 -*-
import os,sys
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import cookielib
import json


reload(sys)
sys.setdefaultencoding('utf-8')

def savetxt(content,filepath):
	with open(filepath.decode('utf-8'),'a') as f:
		f.write(content)

def getcontentxt(questionid):
	#questionid=30787036
	url='https://www.zhihu.com/question/'+questionid
	content=urllib2.urlopen(url).read()
	topicsoup=BeautifulSoup(content,"html.parser")

	#获取话题名
	topicname=''
	topicname=topicsoup.title.string.strip()
	print 'start:保存知乎主题【%s】...'%(topicname)
	filename=re.sub(r'[\.| ]','',topicname)+'.txt'
	savetxt(topicname,'./'+filename)
	#获取话题内容
	topicdetail=topicsoup.find('textarea',class_='content hidden').get_text()
	savetxt('\n\n\t\t\t\t\t***********topicdetail***********\n\n','./'+filename)
	savetxt(re.sub(r'<br>|<br><br>','',topicdetail),'./'+filename)
	savetxt('\n\n\t\t\t\t\t***********topicdetail***********\n\n','./'+filename)
	#print re.sub(r'<br>|<br><br>','',topicdetail)
	#获取评论列表
	startpage=0
	while True:
		answerhtml=getanswerhtml(questionid,startpage)
		if answerhtml=='':
			break
		parseanswer('./'+filename,answerhtml)
		startpage+=10
		
	
	print 'end:保存知乎主题【%s】...'%(topicname)

def parseanswer(filepath,content):
	soup=BeautifulSoup(content,"html.parser")
	answerlist=[]
	answerlist=soup.find_all('div',class_='zm-editable-content clearfix')
	index=0
	savetxt('\n\n\t\t\t\t\t===========answerlist==========\n\n',filepath)
	for ans in answerlist:
		index+=1
		savetxt('\n\n-----------anser %s----------\n\n'%index,filepath)
		savetxt(ans.get_text(),filepath)

	savetxt('\n\n\t\t\t\t\t===========answerlist==========\n\n',filepath)

def getanswerhtml(questionid,start):
	cj=cookielib.CookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}

	url='https://www.zhihu.com/node/QuestionAnswerListV2'
	dicparams={}
	dicparams['url_token']=questionid
	dicparams['offset']=start
	data={'_xsrf':'58118f72af8555e531b69d8d5d25d59c','method':'next','params':'{"pagesize":10}'}
	data['params']=json.dumps(dicparams)
	req=urllib2.Request(url,urllib.urlencode(data),headers)
	content=urllib2.urlopen(req).read()
	msg=''.join(json.loads(content)['msg'])
	return msg



getcontentxt('30787036')


	

