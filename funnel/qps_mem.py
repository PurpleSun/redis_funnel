#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/21 22:58
import time
from functools import wraps


class Funnel(object):
    def __init__(self, capacity, operations, seconds, left_quota=None, leaking_ts=None):
        self.capacity = capacity  # 漏斗容量
        self.operations = operations
        self.seconds = seconds
        self.left_quota = left_quota or capacity  # 漏斗剩余空间
        self.leaking_ts = leaking_ts or time.time()  # 上一次漏水时间
        self.leaking_rate = operations / float(seconds)

    def _make_space(self):
        now_ts = time.time()
        delta_ts = now_ts - self.leaking_ts  # 距离上一次漏水过去了多久
        delta_quota = delta_ts * self.leaking_rate  # 腾出的空间
        if delta_quota < 1:  # 腾的空间过小等待下一次
            return

        self.left_quota += delta_quota  # 增加剩余空间
        if self.left_quota > self.capacity:  # 剩余空间不得高于容量
            self.left_quota = self.capacity
        self.leaking_ts = now_ts  # 记录漏水时间

    def watering(self, quota):
        self._make_space()
        if self.left_quota >= quota:  # 判断剩余空间是否足够
            self.left_quota -= quota
            return (
                True,
                self.capacity,
                self.left_quota,
                -1,
                (self.capacity - self.left_quota) / float(self.leaking_rate)
            )
        else:
            return (
                False,
                self.capacity,
                self.left_quota,
                quota / float(self.leaking_rate),
                (self.capacity - self.left_quota) / float(self.leaking_rate)
            )


def qps(n):
    funnel = Funnel(n, n, 1)

    def outer(f):
        @wraps(f)
        def inner(*args, **kwargs):
            attempt = 0
            while True:
                attempt += 1
                ready, capacity, left_quota, interval, empty_time = funnel.watering(1)
                print "interval: %f" % interval
                if ready:
                    print "attempt: %s" % attempt
                    return f(*args, **kwargs)
                else:
                    time.sleep(interval)

        return inner
    return outer
