#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 13:08
import time

from funnel.qps_mem import qps


@qps(10)
def loop():
    print "current time is %f" % time.time()


while True:
    loop()
