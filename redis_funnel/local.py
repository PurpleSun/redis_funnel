#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/21 22:58
import time
from functools import wraps


class Funnel(object):
    """Local funnel based on memory.
    """

    def __init__(self, capacity, operations, seconds, left_quota=0, leaking_ts=None):
        """
        :param capacity: <int> max capacity of funnel
        :param operations: <int> max operations permitted in specified seconds
        :param seconds: <int> time window for max operations permitted, with second unit
        :param left_quota: <float> left quota of funnel
        :param leaking_ts: <float> latest leaking timestamp, default None
        """
        self.capacity = capacity
        self.operations = operations
        self.seconds = seconds
        self.left_quota = left_quota
        self.leaking_ts = leaking_ts or time.time()
        self.leaking_rate = operations / float(seconds)

    def _make_space(self, quota):
        now_ts = time.time()
        delta_ts = now_ts - self.leaking_ts  # 距离上一次漏水过去了多久
        delta_quota = delta_ts * self.leaking_rate  # 腾出的空间
        if (self.left_quota + delta_quota) < quota:  # 腾的空间过小等待下一次
            return

        self.left_quota += delta_quota  # 增加剩余空间
        if self.left_quota > self.capacity:  # 剩余空间不得高于容量
            self.left_quota = self.capacity
        self.leaking_ts = now_ts  # 记录漏水时间

    def watering(self, quota):
        """
        :param quota: water quota
        :return: a tuple with 5 members, name it as ret
          ret[0]: <bool> return True if there has enough left quota, else False
          ret[1]: <int> funnel capacity
          ret[2]: <float> funnel left quota after watering
          ret[3]: <float> -1 if ret[0] is True, else waiting time until there have enough left quota to watering
          ret[4]: <float> waiting time until the funnel is empty
        """
        self._make_space(quota)
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
    """
    :param n: max qps
    :return: decorated function
    """
    funnel = Funnel(n, n, 1, left_quota=0)

    def outer(f):
        @wraps(f)
        def inner(*args, **kwargs):
            attempt = 0
            while True:
                attempt += 1
                ready, capacity, left_quota, interval, empty_time = funnel.watering(1)
                if ready:
                    return f(*args, **kwargs)
                else:
                    time.sleep(interval)

        return inner
    return outer
