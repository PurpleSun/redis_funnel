#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 12:51
from functools import wraps
import time
import os

import redis


class Funnel(object):
    """Distributed funnel based on redis.
    """

    def __init__(self, group, key, capacity, operations, seconds,
                 redis_host="localhost",
                 redis_port=6379,
                 redis_db=0):
        """
        :param group: <str> key group, e.g. app id or module name
        :param key: <str> key name, used as cache key name, should be business name or method name usually
        :param capacity: <int> max capacity of funnel
        :param operations: <int> max operations permitted in specified seconds
        :param seconds: <int> time window for max operations permitted, with second unit
        :param redis_host: <str> redis host, default "localhost"
        :param redis_port: <int> redis port, default 6379
        :param redis_db: <int> redis db, default 0
        """
        self.group = group
        self.key = key

        self.capacity = capacity
        self.operations = operations
        self.seconds = seconds
        self.leaking_rate = operations / float(seconds)

        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db

        self._watering = self._load()

    def _load(self):
        # register lua script into redis
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        r = redis.Redis(connection_pool=pool)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, "funnel.lua")
        with open(filename) as script:
            lua = script.read()
        watering = r.register_script(lua)
        return watering

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
        ready, capacity, left_quota, interval, empty_time = self._watering(
            keys=[self.group, self.key],
            args=[self.capacity, self.operations, self.seconds, quota])
        interval = float(interval)
        empty_time = float(empty_time)
        return ready, capacity, left_quota, interval, empty_time


def qps_factory(host="localhost", port=6379, db=0):
    """
    :param host: <str> redis host, default "localhost"
    :param port: <int> redis port, default 6379
    :param db: <int> redis db, default 0
    :return: qps decorator
    """
    def qps(group, key, n):
        """
        :param group: key group, e.g. app id or module name
        :param key: key name, used as cache key name, should be business name or method name usually
        :param n: max qps
        :return: decorated function
        """
        funnel = Funnel(group, key, n, n, 1, redis_host=host, redis_port=port, redis_db=db)

        def outer(f):
            @wraps(f)
            def inner(*args, **kwargs):
                attempt = 0
                while True:
                    attempt += 1
                    ready, capacity, left_quota, interval, empty_time = funnel.watering(1)
                    if ready == 0:
                        return f(*args, **kwargs)
                    else:
                        time.sleep(interval)

            return inner
        return outer
    return qps
