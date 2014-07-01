#-*- coding:utf-8 -*-

from gevent.pool import Pool

_MAX_GREENLET_NUM = 1000000
gpool = Pool(_MAX_GREENLET_NUM)

