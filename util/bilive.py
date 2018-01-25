#!/usr/bin/python3
# coding = utf-8

import requests

class Bilive(object):
	"""docstring for Bilive"""
	def __init__(self):
		self.update()

	def play(self,room_id):
		durls = requests.get('https://api.live.bilibili.com/api/playurl?cid=' + str(self.room_ids[room_id]) +'&otype=json&quality=0&platform=web').json()
		vdo_links = durls['durl']
		self.play_url = [x['url'] for x in vdo_links]

		import subprocess
		subprocess.call('mpv' + ' \"' + self.play_url[0] + '\"', shell = True)

	def update(self):
		self.room_ids = []
		self.room_titles = []
		for page_num in range(20):
			content = requests.get('http://api.live.bilibili.com/area/liveList?area=movie&order=online&page=' + str(page_num)).json()
			raw_data = content['data']
			if raw_data == []:
				break
			else:
				self.room_ids.extend([x['roomid'] for x in raw_data])
				self.room_titles.extend([x['title'] for x in raw_data])
	
	def search(self,key_words):
		def filt_live(num_title):
			i = num_title[0]
			x = num_title[1]
			return reg_kword.search(x)
		import re
		reg_kword = re.compile(key_words)
		self.sear_result = list(filter(filt_live, enumerate(self.room_titles)))

	def export(self):
		pass