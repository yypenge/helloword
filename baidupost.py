#encoding:utf-8
import os,sys
import urllib
import urllib2
import cookielib
import re
from bs4 import BeautifulSoup,Comment
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


reload(sys)
sys.setdefaultencoding('utf-8')

#发送邮件
def sendmail():
	sender = 'yypenge@163.com'
	password='yang2016'
	smtpserver='smtp.163.com'
	receivers = ['yypenge@163.com'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

	#创建一个带附件的实例
	message = MIMEMultipart()
	message['From'] = Header("彭阳阳", 'utf-8')
	message['To'] =  Header("彭阳阳", 'utf-8')
	subject = 'Python SMTP 邮件测试'
	message['Subject'] = Header(subject, 'utf-8')

	#邮件正文内容
	message.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))

	# 构造附件1，传送当前目录下的 test.txt 文件
	att1 = MIMEText(open('./post.zip', 'rb').read(), 'base64', 'utf-8')
	att1["Content-Type"] = 'application/octet-stream'
	# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
	att1["Content-Disposition"] = 'attachment; filename="post.zip"'
	message.attach(att1)

	smtpObj = smtplib.SMTP('smtp.163.com',25)
	smtpObj.set_debuglevel(1)
	smtpObj.login('yypenge@163.com',password)
	smtpObj.sendmail('yypenge@163.com', ['yypenge@163.com'], message.as_string())
	smtpObj.quit()


#保存文档
def savetxt(content,filepath):
	with open(filepath.decode('utf-8'),'a') as f:
		f.write(content)

#帖子的详细内容
def getpostdata(posthref,postname):

	filepath='./post/%s.txt'%postname
	savetxt('\t\t\t\t[%s]\n\n\n'%postname,filepath)

	ckjar = cookielib.MozillaCookieJar(os.path.join('./', 'cookies.txt'))
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(ckjar))

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
	req=urllib2.Request(posthref,None,headers)
	content=urllib2.urlopen(req).read().decode('utf-8')

	with open('./biena.html','w') as f :
		f.write(content) 
	soup=BeautifulSoup(content,'html.parser')
	
	answerlist=soup.find_all('div',class_='l_post l_post_bright j_l_post clearfix  ')
	savetxt('\t\t\t\t[评论列表]\n\n',filepath)
	floor=0
	for ans in answerlist:
		floor+=1
		#层主
		d_author=ans.contents[1] 

		author_name=d_author.find('a',class_='p_author_name').get_text()
		#层主评论内容 d_post_content j_d_post_content 
		d_author_content=ans.contents[2] 
		if not d_author_content.find('div',class_='p_content '):
			continue
		author_content=d_author_content.find('div',class_='p_content ').get_text()
		savetxt('[%s楼]*%s*:%s\n'%(floor,author_name,author_content),filepath)
		#回复层主lzl_cnt
		#author_reply_list=d_author_content.find_all('div',class_='lzl_cnt')
		#print len(author_reply_list)
		#for author_reply in author_reply_list:
		#	print author_reply.get_text()

	print 'end...'
		


	 
	
#帖子的列表
def getdota2postlist(startpage):
	ckjar = cookielib.MozillaCookieJar(os.path.join('./', 'cookies.txt'))
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(ckjar))

	uri="http://tieba.baidu.com"
	url="http://tieba.baidu.com/f?kw=dota2&ie=utf-8&pn=%s"%startpage
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
	req=urllib2.Request(url,None,headers)
	content=urllib2.urlopen(req).read().decode('utf-8')
	
	soup=BeautifulSoup(re.sub(r'<!--|-->','',content),'html.parser')
	
	postlist=soup.find_all('a',class_='j_th_tit')

	for post in postlist:
		print post
		#帖子的名字a
		postname=re.sub(r'\.|\。|\?','',post['title'])
		posthref=uri+post['href']
		print ' 正在保存帖子【%s】'%postname
		getpostdata(posthref,postname)
		
#压缩文件夹
def zipdir(dirname,zipfilename):
	filelist = [] 
	if os.path.isfile(dirname): 
		filelist.append(dirname) 
	else :	
		for root, dirs, files in os.walk(dirname): 
			for name in files: 
				filelist.append(os.path.join(root, name)) 

	zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED) 
	for tar in filelist: 
		arcname = tar[len(dirname):] 
		#print arcname 
		zf.write(tar,arcname) 
	zf.close() 		

#测试专用		
def test():
	content='军团这鬼英雄到底该怎么玩。。。'
	result=re.sub(r'\.|\。|\?','',content)
	print result


#getpostdata('http://tieba.baidu.com/p/4571362257','这张图大概是多少分的，朋友跟我吹逼他蓝猫多厉害.....')
#getdota2postlist(5)
#zipdir('./post','post.zip')
sendmail()
