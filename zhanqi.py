import urllib.request as http
import re
import codecs

#定义获取id和标题的函数
def get_index_sources():
	sid = []
	title = []
	count = 1
	while(count < 10):
		content = http.urlopen('http://www.zhanqi.tv/api/static/game.lives/45/30-'+str(count)+'.json').read().decode('UTF-8')
		count += 1
		temp_sid = re.findall('(?<=videoId":")[^"]*',content)
		if(not temp_sid):
			break
		title = title + re.findall('(?<=title":")[^"]*',content)
		sid = sid + temp_sid
	write_m3u8(sid,title)

#定义将直播源写入的函数
def write_m3u8(sid,title):
	file = codecs.open('zhanqi.dpl','w+','utf-8')
	file.write('DAUMPLAYLIST'+'\n')	
	filem = codecs.open('zhanqim.dpl','w+','utf-8')
	filem.write('DAUMPLAYLIST'+'\n')
	n = 1
	for(i,j)in zip(sid,title):
		file.write(str(n)+"*file*http://wshdl.load.cdn.zhanqi.tv/zqlive/"+i+'.flv\n')
		file.write(str(n)+"*title*"+j+'\n')
		filem.write(str(n)+"*file*http://dlhls.cdn.zhanqi.tv/zqlive/"+i+'.m3u8\n')
		filem.write(str(n)+"*title*"+j+'\n')
		n += 1
	file.close()
	filem.close()

if __name__ == '__main__':
	get_index_sources()