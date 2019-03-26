#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/26 19:49
import time

import redis

from redis_funnel.distributed import Funnel


def benchmark(f, times):
    def wrapper(*args, **kwargs):
        elapsed = time.time()
        for _ in xrange(times):
            f(*args, **kwargs)
        elapsed = time.time() - elapsed
        return times / float(elapsed)

    return wrapper


pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
r = redis.Redis(connection_pool=pool)

print "benchmarking redis raw get..."
qps = benchmark(r.get, 100000)("name")
print "max qps: %s\n" % qps

print "benchmarking redis lua get..."
get = r.register_script("return redis.call('GET', KEYS[1])")
qps = benchmark(get, 100000)("name")
print "max qps: %s\n" % qps

print "benchmarking redis lua funnel..."
funnel = Funnel("1000001", "test", 5000, 5000, 1, redis_host="localhost", redis_port=6379, redis_db=0)
qps = benchmark(funnel.watering, 100000)(1)
print "max qps: %s\n" % qps
