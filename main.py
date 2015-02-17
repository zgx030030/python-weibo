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
from lib import AutomaticPost
#日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='myapp.log',filemode='w')

APP_KEY = "801549337"
APP_SECRET = "370bdd54b9870c1f26a9dd0bca1ce76a"
CALLBACK_URL = "https://www.zh30.com/api/qqweibo/"
ACCESS_TOKEN = "aa79a7b96ad5ebf8f6d1871a89f58110"
OPENID = "AEDA52D7B48ECA515146D088F77F7574"
IMG_EXAMPLE = "example.png"

coding = sys.getfilesystemencoding()

#定时任务列表
autoPostTaskListT = []
autoPostTaskListC = []
#标记
flag = False

#返回接口api
def getAPI():
	oauth = OAuth2Handler()
	oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
	oauth.set_access_token(ACCESS_TOKEN)
	oauth.set_openid(OPENID)
	api = API(oauth)
	return api

#自动评论@我的微博
def autoCommentAt():
	r = api.get.statuses__mentions_timeline(format="json", pageflag=2, pagetime=1414735332,reqnum=10,lastid=460257016911748, type=0, contenttype=0)
	for o in r.data.info:
		print o.id,',',o.timestamp
		print '@我的内容：',o.text
		comment = urllib2.urlopen('http://www.tuling123.com/openapi/api?key=d4408411d473fab8aba0de55c8079f4a&info='+o.text.encode('utf-8').replace('@郑晓','').replace('@zheng0000','')).read()
		comment = eval(comment)
		print '回复的内容：', comment['text'].decode('utf-8')

		tmp = api.post.t__comment(format="json", content=comment['text'], clientip='222.173.94.214', reid=o.id)
		if tmp.errcode ==0:
			print '回复成功'
			break
		time.sleep(2)

#显示主菜单
def showMainMenu():
	os.system('cls')
	print '*'*50
	print '欢迎使用 腾讯微博小管家 测试版'
	print '程序使用Python编写，基于Python-SDK'
	print 'by zheng0000'
	print ''
	print '回复0 退出程序'
	print '回复1 设置/关闭 自动发布功能'
	print '回复2 设置/关闭 自动评论@我的微博功能'
	print '回复3 设置/关闭 自动抢沙发功能 开发中...'
	print '回复9 显示当前状态'
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
			#自动发布
			p = re.compile(r'\s+')
			while True:
					code = raw_input('设置或修改定时发布任务：')
					if code=='':
						showMainMenu()
						break
					code = p.sub(' ', code)
					args = code.split(' ')
					api = getAPI()
					autopost = AutomaticPost.AutomaticPost(api, logging)
					operation = {
						'add': lambda x,y:autopost.add_task(x,y),
						'del': lambda x,y:del_auto_post_task(x),
						'show':lambda x,y:autopost.show_task()
						}
					while len(args)<3:
						args.append(' ')
					print operation[args[0]](args[1],args[2])
				
		if code == 2:
			#自动评论
			pass
		if code == 3:
			#自动抢沙发
			pass
