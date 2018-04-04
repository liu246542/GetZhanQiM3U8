#! /usr/local/ python3
# coding = utf-8

# import threading
from util.zhanlive import Zhanlive
from util.bilive import Bilive

if __name__ == '__main__':
    print('[1]bilibili\n[2]zhanqi\n')
    plat_flag = input('请选择:')
    if(plat_flag == '1'):
        app = Bilive()
    else :
        app = Zhanlive()
    key_word = input('请输入关键词：')
    app.search(key_word)
    if len(app.sear_result) == 0:
        print('没有找到')
    elif len(app.sear_result) == 1:
        app.play(app.sear_result[0][0])
    else:
        print('请选择:')
        print('{0:-^10}|{1:-^10}'.format('index','title'))
        for item in app.sear_result:
            print('{0:-^10}|{1:-^10}'.format(item[0],item[1]))
        play_num = input('请输入序号：')
        app.play(int(play_num))
