# -*- coding:utf-8 -*-
import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.header import Header
import urllib
import urllib2
import re

def sendMail():
	from_addr = raw_input('From: ')
	password = raw_input('Password: ')
	# 输入SMTP服务器地址:
	smtp_server = raw_input('SMTP server: ')
	# 输入收件人地址:
	to_addr = raw_input('To: ')

	msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')

	server = smtplib.SMTP(smtp_server, 25) # SMTP协议默认端口是25
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()



#在Bing上下载明星的图片链接
class Spider:

	def __init__(self, fileName):
		
		self.fileName = fileName

		
	def getContents(self,name,start,pageSize):
		page = self.getPages(name,start,pageSize)
		pattern = re.compile(r'<a.*?surl:\&quot\;(.*?)\&quot\;.*?imgurl:\&quot\;(.*?)\&quot\;.*?>',re.S)
		items = re.findall(pattern,page)
		list0=[]
		for i in items:
			listmp=[]
			listmp.append('[links]'+i[0])
			listmp.append('[refer]'+i[1])
			list0.append(listmp)
		return list0

	#获取单页面的links和refer	
	def getPages(self,name,start,pageSize):
		#封装数据

		values={}
		values['q']=name
		values['first']=start
		values['count']=pageSize
		data=urllib.urlencode(values)
		request=urllib2.Request('http://cn.bing.com/images/async?'+data)
		
		logging.error('请求Bing[王菲]。。')
		response=urllib2.urlopen(request)
		content=response.read()
		return content
	#保存文件	
	def saveTxt(self,name,items):
		f='D:/Python27/workspace/star/'+name+'.txt'
		with open(unicode(f,'utf-8'),'w') as ff:
			for item in items:
				print '正在保存%s'%item[0]
				print '正在保存%s'%item[1]
				ff.write(item[0]+'\n')
				ff.write(item[1]+'\n')
			ff.close()
	#读取带有name的txt文件
	def readTxt(self):
		nameList=[]
		with open(unicode(self.fileName,'utf-8'),'r') as f:
			for line in f.readlines():
				name=line.strip();
				print name
				nameList.append(name)
			f.close()	
		return nameList


		
if __name__ == '__main__':
 	
	spider = Spider('D:/Python27/workspace/star/name.txt')
	nameList=spider.readTxt()
	#遍历名单中的名字
	for name in nameList:
		sumList=[]
		sumList=spider.getContents(name,1,35)
		spider.saveTxt(name,sumList)


