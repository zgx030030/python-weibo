#!/usr/bin/env python
#coding:utf-8

import re, time, threading

#定时自动发布微博类
class AutomaticPost:
	autoPostTaskListT = []
	autoPostTaskListC = []
	api  = None
	flag = False
	log = None
	def __init__(self, api, log):
		self.api = api
		self.log = log
	#发布
	def autoPost(self, t, c):
		while int(time.time()) < t:
			time.sleep(1)
		r = self.post.t__add(format="json", content=c.decode('gbk'))
		if r.errcode==0:
			self.log.info('定时发送成功！')
		else:
			self.log.info('定时发送失败！' + str(r.errcode))
	#检查任务时间
	def threading_do_task(self):
		while True:
			if len(self.autoPostTaskListT) == 0:
				self.flag = False
			min_t = min(self.autoPostTaskListT)
			if int(time.time()) < min_t:
				sleepSecond = min_t - int(time.time())
				self.log.info('sleep' + str(sleepSecond) + '秒...')
				time.sleep(sleepSecond)
				self.log.info('sleep end')
				continue
			for i in xrange(self.autoPostTaskListT.count(min_t)):
				index = self.autoPostTaskListT.index(min_t)
				self.autoPost(self.autoPostTaskListT[index], self.autoPostTaskListC[index])
				self.log.info('执行发布：'+str(self.autoPostTaskListT[index])+"\t"+self.autoPostTaskListC[index])
				del self.autoPostTaskListT[index]
				del self.autoPostTaskListC[index]


	#添加定时任务
	def add_task(self, t, c):
		p = "%Y-%m-%d/%H:%M:%S"
		if re.search('^\d{2}:\d{2}:\d{2}$', t):
			t = time.strftime('%Y-%m-%d/') + t
		if not re.search('^\d{4}-\d{2}-\d{2}/\d{2}:\d{2}:\d{2}', t):
			self.log.debug('日期格式错误')
			return False
		t = int(time.mktime(time.strptime(t, p)))
		self.autoPostTaskListT.append(t)
		self.autoPostTaskListC.append(c)
		if not self.flag:
			self.flag = True
			threading.Thread(target=self.threading_do_task, args=()).start()
		return True

	#删除定时任务
	def del_task(self, i):
		try:
			i = int(i)
			del self.autoPostTaskListT[i]
			del self.autoPostTaskListC[i]
			return True
		except:
			return False
	#列出当前任务列表
	def show_task(self):
		try:
			print '当前队列中的任务有：'
			for i in xrange(len(self.autoPostTaskListT)):
				print i, "\t", self.autoPostTaskListT[i], "\t", self.autoPostTaskListC[i]
			return True
		except:
			return False

if __name__ == '__main__':
	print '程序入口为/main.py'
	raw_input()
