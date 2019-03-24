#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/23 17:22
from functools import wraps
import time

import redis

from timeit import timeit


def qps_factory(host="localhost", port=6379, db=0):
    def _qps(group, key, n):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        r = redis.Redis(connection_pool=pool)

        with open("funnel.lua") as script:
            lua = script.read()
        funnel = r.register_script(lua)
        funnel = timeit(funnel)

        def outer(f):
            @wraps(f)
            def inner(*args, **kwargs):
                attempt = 0
                while True:
                    attempt += 1
                    ready, capacity, left_quota, interval, empty_time = funnel(keys=[group, key], args=[n, n, 1, 1])
                    interval = float(interval)
                    print "interval: %f" % interval
                    if ready == 0:
                        print "attempt: %s" % attempt
                        return f(*args, **kwargs)
                    else:
                        time.sleep(interval)
            return inner
        return outer
    return _qps


qps = qps_factory()


@qps("1000002", "delete", 50)
def loop():
    print "current time is %f" % time.time()


while True:
    loop()
