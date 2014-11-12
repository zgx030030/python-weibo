#!/usr/bin/env python
# -*- coding: cp936 -*-

import threading
import logging
import urllib2
import time
import sys
import re
import os
from tweibo import *

#��־
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='myapp.log',filemode='w')

APP_KEY = "801549337"
APP_SECRET = "370bdd54b9870c1f26a9dd0bca1ce76a"
CALLBACK_URL = "https://www.zh30.com/api/qqweibo/"
ACCESS_TOKEN = "aa79a7b96ad5ebf8f6d1871a89f58110"
OPENID = "AEDA52D7B48ECA515146D088F77F7574"
IMG_EXAMPLE = "example.png"

coding = sys.getfilesystemencoding()

#��ʱ�����б�
autoPostTaskListT = []
autoPostTaskListC = []
#���
flag = False

#���ؽӿ�api
def getAPI():
	oauth = OAuth2Handler()
	oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
	oauth.set_access_token(ACCESS_TOKEN)
	oauth.set_openid(OPENID)
	api = API(oauth)
	return api
#�Զ�����ִ�еķ���
#t ��ʱʱ���  c ��������
def autoPost(t, c):
	while int(time.time())<t:
		time.sleep(1)
	oauth = OAuth2Handler()
	oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
	oauth.set_access_token(ACCESS_TOKEN)
	oauth.set_openid(OPENID)
	api = API(oauth)
	#��ʼ����
	r = api.post.t__add(format="json", content=c.decode('gbk'), clientip='222.173.94.214')
	if r.errcode==0:
		print '��ʱ���ͳɹ���'.decode('utf-8').encode(coding)
	else:
		print '����ʧ�� ������룺'.decode('utf-8').encode(coding), r.errcode

#�������ʱ���߳�
def threading_do_task():
	global flag
	while True:
		logging.debug('in threading....')
		if len(autoPostTaskListT) ==0:
			flag = False
			break
		min_t = min(autoPostTaskListT)
		if int(time.time())<min_t:
			time.sleep(1)
			continue
		logging.debug('min_t:'+str(min_t))
		for i in xrange(autoPostTaskListT.count(min_t)):
			index = autoPostTaskListT.index(min_t)
			logging.debug('index:'+str(index) )
			logging.debug( 'ִ�з���:'+autoPostTaskListT[index]+"\t"+autoPostTaskListC[index])
			del autoPostTaskListT[index]
			del autoPostTaskListC[index]
		time.sleep(1)
#��Ӷ�ʱ����
def add_auto_post_task(t,c):
		global flag
		p = '%Y-%m-%d/%H:%M:%S'
		t = int(time.mktime(time.strptime(t, p)))
		autoPostTaskListT.append(t)
		autoPostTaskListC.append(c)
		if not flag:
			flag = True
			threading.Thread(target=threading_do_task, args=()).start()
		return True
#ɾ����ʱ����
def del_auto_post_task(i):
	try:
		i = int(i)
		del autoPostTaskListT[i]
		del autoPostTaskListC[i]
		return True
	except:
		return False
#�г���ǰ��ʱ�����б�
def show_auto_post_task():
	try:
		for i in xrange(len(autoPostTaskListT)):
			print i,"\t",autoPostTaskListT[i], "\t", autoPostTaskListC[i]
		return True
	except:
		return False

#�Զ�����@�ҵ�΢��
def autoCommentAt():
	r = api.get.statuses__mentions_timeline(format="json", pageflag=2, pagetime=1414735332,reqnum=10,lastid=460257016911748, type=0, contenttype=0)
	for o in r.data.info:
		print o.id,',',o.timestamp
		print '@�ҵ����ݣ�',o.text
		comment = urllib2.urlopen('http://www.tuling123.com/openapi/api?key=d4408411d473fab8aba0de55c8079f4a&info='+o.text.encode('utf-8').replace('@֣��','').replace('@zheng0000','')).read()
		comment = eval(comment)
		print '�ظ������ݣ�', comment['text'].decode('utf-8')

		tmp = api.post.t__comment(format="json", content=comment['text'], clientip='222.173.94.214', reid=o.id)
		if tmp.errcode ==0:
			print '�ظ��ɹ�'
			break
		time.sleep(2)

#��ʾ���˵�
def showMainMenu():
	os.system('cls')
	print '*'*50
	print '��ӭʹ�� ��Ѷ΢��С�ܼ� ���԰�'
	print '����ʹ��Python��д������Python-SDK'
	print 'by zheng0000'
	print ''
	print '�ظ�0 �˳�����'
	print '�ظ�1 ����/�ر� �Զ���������'
	print '�ظ�2 ����/�ر� �Զ�����@�ҵ�΢������'
	print '�ظ�3 ����/�ر� �Զ���ɳ������ ������...'
	print '�ظ�9 ��ʾ��ǰ״̬'
	print '*'*50
	
if __name__ == '__main__':
	showMainMenu()
	while True:
		try:
			code = int(raw_input())
		except:
			code = 0
		if code == 0:
			break
		if code == 1:
			#�Զ�����
			p = re.compile(r'\s+')
			while True:
					code = raw_input('���û��޸Ķ�ʱ��������')
					if code=='':
						showMainMenu()
						break
					code = p.sub(' ', code)
					args = code.split(' ')
					operation = {
						'add': lambda x,y:add_auto_post_task(x,y),
						'del': lambda x,y:del_auto_post_task(x),
						'show':lambda x,y:show_auto_post_task()
						}
					while len(args)<3:
						args.append(' ')
					print operation[args[0]](args[1],args[2])
				
		if code == 2:
			#�Զ�����
			pass
		if code == 3:
			#�Զ���ɳ��
			pass
