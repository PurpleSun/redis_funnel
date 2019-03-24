#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/23 23:23
import time


def timeit(f):
    mem = {
        "count": 0,
        "time": 0
    }

    def wrapper(*args, **kwargs):
        elapsed = time.time()
        ret = f(*args, **kwargs)
        elapsed = (time.time() - elapsed) * 1000
        mem["count"] += 1
        mem["time"] += elapsed
        print "==>elapsed: %s ms | time: %s ms, count: %s | avg: %s ms" \
              % (elapsed, mem["time"], mem["count"], mem["time"] / float(mem["count"]))
        return ret

    return wrapper
