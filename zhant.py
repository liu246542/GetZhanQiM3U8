import threading

from util.zhanlive import Zhanlive

zhanqi = Zhanlive()

# threading.active_count()

thd1 = threading.Thread(target = zhanqi.play, args = ([55]), name = 'test1')

thd1.start()
