#!/usr/bin/python3
# coding = utf-8

import requests

def get_pages():
	room_ids = []
	room_titles = []
	for pageNum in range(20):
		content = requests.get('http://api.live.bilibili.com/area/liveList?area=movie&order=online&page=' + str(pageNum)).json()
		raw_data = content['data']
		if raw_data == [] :
			break
		else:
			room_ids.extend(list(map(lambda x : x['roomid'], raw_data)))
			room_titles.extend(list(map(lambda x: x['title'],raw_data)))		
	return room_ids,room_titles

def get_hls(room_id):
	durls = requests.get('https://api.live.bilibili.com/api/playurl?cid=' + str(room_id) +'&otype=json&quality=0&platform=web').json()
	vdo_links = durls['durl']
	return list(map(lambda x: x['url'],vdo_links))

'''
def parse_roomid(room_ids):
	paly_list = list(map(get_hls,room_ids))
	return paly_list
'''

def live_play(play_url):
	import subprocess
	subprocess.call('mpv' + ' \"' + play_url + '\"', shell = True)

def live_search(title):
	key_words = input('请输入关键词：')
	def filt_live(num_title):
		i = num_title[0]
		x = num_title[1]
		return reg_kword.search(x)
	import re
	reg_kword = re.compile(key_words)
	flag_live = list(filter(filt_live, enumerate(title)))
	return flag_live

if __name__ == '__main__':
	roomids,roomtitles = get_pages()
	# plist = parse_roomid(roomids)
	i = 0
	while i < 10:
		flags = live_search(roomtitles)
		if len(flags) == 0:
			again_flag = input('没有找到，是否重试<y/n?>')
			if(again_flag == 'y'):
				continue
			else:
				break
		elif len(flags) == 1:
			# live_play(plist[flags[0][0]][0])
			play_url = get_hls(roomids[flags[0][0]])
			live_play(play_url[0])
			i += 1
			continue
		else:
			print('请选择：')
			print('{0:-^10}|{1:-^10}'.format('index','title'))
			for item in flags:
				print('{0:-^10}|{1:-^10}'.format(item[0],item[1]))
			play_num = input('请输入序号：')
			# live_play(plist[int(play_num)][0])
			play_url = get_hls(roomids[int(play_num)])
			live_play(play_url[0])
			i += 1