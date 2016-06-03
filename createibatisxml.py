#encoding:utf-8
import os,sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


#USER_INFO转成userInfo
def transfstr(s):
	strlist=re.split(r'_',s)
	index=0
	result=''
	for ss in strlist:
		if index==0:
			result+=ss.lower()
		else:
			result+=ss[0]+ss[1:].lower()
		index+=1
	return result

#读取文件 <result property="id" column="ID"/>
def readtxt(inputpath,outputpath):
		with open(inputpath,'r') as f:
			content=f.read().strip()
			for field in content.split(r','):
				savetxt(outputpath,'<result property="%s" column="%s"/>'%(transfstr(field),field))

			savetxt(outputpath,'\n\n')
			savetxt(outputpath,insert(content))

			savetxt(outputpath,'\n\n')
			savetxt(outputpath,select(content))

			print'end...'

#sql 模板 insert into table (field,field) values (#field#,#field#)
def insert(content):
	s=[]
	for ss in content.split(r','):
		s.append('#%s#'%transfstr(ss))
	return  "INSERT INTO TABLE (%s) VALUES (%s)"%(content,",".join(s))

#sql 模板 select * from table 
def select(content):
	return "SELECT %s FROM TABLE"%content


#写文件 python createibatisxml.py  './attr.txt','./attresult.txt'
def savetxt(filepath,content):
	with open(filepath,'a') as f:
		f.write(content+'\n')

if __name__ == '__main__':
	inputpath=sys.argv[1]
	outputpath=sys.argv[2]

	readtxt(inputpath,outputpath)
