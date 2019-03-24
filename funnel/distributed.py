#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 12:51
from functools import wraps
import time
import os

import redis

from funnel.timeit import timeit


class Funnel(object):
    def __init__(self, group, key, capacity, operations, seconds,
                 redis_host="localhost",
                 redis_port=6379,
                 redis_db=0):
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
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        r = redis.Redis(connection_pool=pool)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, "funnel.lua")
        with open(filename) as script:
            lua = script.read()
        watering = r.register_script(lua)
        watering = timeit(watering)
        return watering

    def watering(self, quota):
        return self._watering(keys=[self.group, self.key],
                              args=[self.capacity, self.operations, self.seconds, quota])


def qps_factory(host="localhost", port=6379, db=0):
    def qps(group, key, n):
        funnel = Funnel(group, key, n, n, 1, redis_host=host, redis_port=port, redis_db=db)

        def outer(f):
            @wraps(f)
            def inner(*args, **kwargs):
                attempt = 0
                while True:
                    attempt += 1
                    ready, capacity, left_quota, interval, empty_time = funnel.watering(1)
                    interval = float(interval)
                    print "interval: %f" % interval
                    if ready == 0:
                        print "attempt: %s" % attempt
                        return f(*args, **kwargs)
                    else:
                        time.sleep(interval)

            return inner
        return outer
    return qps
