#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 12:51
from functools import wraps
import time
import os

import redis

from funnel.timeit import timeit


def qps_factory(host="localhost", port=6379, db=0):
    def _qps(group, key, n):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        r = redis.Redis(connection_pool=pool)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(dir_path, "funnel.lua")
        with open(filename) as script:
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
