# signals.py
from gitdb.util import exists
from scrapy.signalmanager import SignalManager

# 信号
spider_stop_signal = SignalManager()

existed_signal = 1
