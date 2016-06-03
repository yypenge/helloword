#encoding:utf-8
import os,sys
from random import choice

reload(sys)
sys.setdefaultencoding('utf-8')


#快速排序
def quicksort(ll):
	i=0
	j=len(ll)-1
	p=ll[0]

	while i<j:
		
		while i<j and p<=ll[j]:
			j-=1
		print 'i=%s;j=%s;p=%s'%(i,j,p)
		end=ll[j]
		ll[j]=p
		ll[0]=end

			

		while i<j and p>=ll[i]:
			i+=1
		print 'i=%s;j=%s;p=%s'%(i,j,p)
		start=ll[i]
		ll[i]=p 
		ll[j]=start

		print ll
#冒泡排序
def bubblesort(ll):
	compare=0
	j=len(ll)
	while j>0:
		j-=1
		for i in xrange(j):
			behind=ll[j]
			previous=ll[i]
			compare+=1
			if previous>behind:
				ll[j]=previous
				ll[i]=behind
	print '排序后ll=%s 比较次数%s'%(ll,compare)
#递归冒泡
def bubble(lll,num):
	if num==0:
		ll=lll[:]
		surplus=[]
	else:

		ll=lll[:-num]
		surplus=lll[-num:]
	j=len(ll)
	
	if j<=1:
		return lll
	else:
		for i in xrange(j-1):
			first=ll[i]
			second=ll[i+1]
			if first>second:
				ll[i]=second
				ll[i+1]=first
		num+=1
		ll.extend(surplus)
		return bubble(ll,num)


def test(num):

	listtest=[2,5,13,12,19,26,55,46]
	l1=listtest
	listt=listtest[:-num]
	print listt
	 


#test(0)
result=bubble([2,5,13,12,19,26,55,46],0)
print result

			
