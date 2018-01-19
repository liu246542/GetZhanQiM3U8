#!/usr/bin/python3
# coding=utf-8
import requests
import codecs
import sys
import platform

#定义获取id和标题的函数
def get_index_sources():
	sid = []
	title = []
	count = 1
	while(count < 10):
		content = requests.get("http://www.zhanqi.tv/api/static/v2.1/game/live/45/30/" + str(count) + ".json").json()
		count += 1
		temp_sid = content['data']['rooms'] # [0]['videoId']
		if(temp_sid == []):
			break
		else:
			sid.extend([x['videoId'] for x in content['data']['rooms']])
			title.extend([x['title'] for x in content['data']['rooms']])
	return sid,title

def process_m3u8(sid):
	m3u8_list = list(map(lambda x : 'http://dlhls.cdn.zhanqi.tv/zqlive/' + x + '.m3u8',sid))
	return m3u8_list

def zhan_play(m3u8_list,i):
	import subprocess
	if(platform.system() == "Linux"):
		subprocess.call('mpv' + ' \"' + m3u8_list[i] + '\"',shell = True)
	elif(platform.system() == "Windows"):
		subprocess.call("&\'C:\\Program Files\\PotPlayer\\PotPlayerMini64.exe\'" + ' \"' + m3u8_list[i] + '\"')

#定义将直播源写入的函数
def write_m3u8(sid,title):
	file = codecs.open('zhanqi.dpl','w+','utf-8')
	file.write('DAUMPLAYLIST'+'\n')	
	filem = codecs.open('zhanqim.dpl','w+','utf-8')
	filem.write('DAUMPLAYLIST'+'\n')
	filel = codecs.open('zhanqil.txt','w+','utf-8')
	n = 1
	for(i,j)in zip(sid,title):
		file.write(str(n)+"*file*http://wshdl.load.cdn.zhanqi.tv/zqlive/"+i+'.flv\n')
		file.write(str(n)+"*title*"+j+'\n')
		filem.write(str(n)+"*file*http://dlhls.cdn.zhanqi.tv/zqlive/"+i+'.m3u8\n')
		filem.write(str(n)+"*title*"+j+'\n')
		filel.write(j+'\n')
		filel.write("http://dlhls.cdn.zhanqi.tv/zqlive/"+i+'.m3u8\n')
		n += 1
	file.close()
	filem.close()
	filel.close()

def zhan_search(title):
	key_words = input("请输入关键词：")
	def filt_zhan(num_title):
		i = num_title[0]
		x = num_title[1]
		return reg_kword.search(x)
	import re
	reg_kword = re.compile(key_words)
	flag_zhan = list(filter(filt_zhan, enumerate(title)))
	return flag_zhan
	# print(title)
	# print(flag_zhan)


if __name__ == '__main__':
	sid,title = get_index_sources()
	m3u8_list = process_m3u8(sid)
	i = 0
	while i < 10:
		flags = zhan_search(title)
		if len(flags) == 0:
			again_flag = input('没有找到，是否重试<y/n?>')
			if(again_flag == 'y'):
				continue
			else:
				break
		elif len(flags) == 1:
			zhan_play(m3u8_list,flags[0][0])
			break
		else:
			print('请选择:')
			# print(flags)
			print('{0:-^10}|{1:-^10}'.format('index','title'))
			for item in flags:
				print('{0:-^10}|{1:-^10}'.format(item[0],item[1]))
			play_num = input('请输入序号：')
			zhan_play(m3u8_list,int(play_num))
			break
		i += 1