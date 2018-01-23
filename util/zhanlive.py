#!/usr/bin/python3
# coding = utf-8

class Zhanlive(object):
	"""docstring for Zhanlive"""
	def __init__(self):
		self.update()

	def play(self,pindex):
		import subprocess
		import platform
		if(platform.system() == 'Linux'):
			subprocess.call('mpv' + ' \"' + self.plist[pindex] + '\"',shell = True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		elif(platform.system() == "Windows"):
			subprocess.call('C:\\Program Files\\PotPlayer\\PotPlayerMini64.exe' + ' ' + self.plist[pindex])
	
	def update(self):
		'''获取id和标题'''
		import requests
		self.sid = []
		self.title = []

		count = 1
		while(count < 10):
			content = requests.get("http://www.zhanqi.tv/api/static/v2.1/game/live/45/30/" + str(count) + ".json").json()
			count += 1
			temp_sid = content['data']['rooms'] # [0]['videoId']
			if(temp_sid == []):
				break
			else:
				self.sid.extend([x['videoId'] for x in content['data']['rooms']])
				self.title.extend([x['title'] for x in content['data']['rooms']])
				self.plist = ['http://dlhls.cdn.zhanqi.tv/zqlive/' + x + '.m3u8' for x in self.sid]

	def search(self,keyword):		
		def filt_zhan(num_title):
			i = num_title[0]
			x = num_title[1]
			return reg_kword.search(x)
		
		import re
		reg_kword = re.compile(keyword)
		self.searesult = list(filter(filt_zhan,enumerate(self.title)))

	def export(self):
		import codecs
		fileObj = codecs.open('zhanqiLive.dpl','w+','utf-8')
		fileObj.write('DAUMPLAYLIST\n')
		n = 1
		for(i,j) in zip(self.title,self.plist):
			fileObj.write(str(n) + '*file*' + j + '\n')
			fileObj.write(str(n) + '*title*' + i + '\n')
			n += 1
		fileObj.close()