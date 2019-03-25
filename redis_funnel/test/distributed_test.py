#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/23 17:22
import time

from redis_funnel.distributed import qps_factory

qps = qps_factory()


@qps("1000001", "test", 100)
def loop():
    print "current time is %f" % time.time()


while True:
    loop()
