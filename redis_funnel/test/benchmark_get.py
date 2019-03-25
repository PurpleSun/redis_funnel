#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/23 17:22
import redis

from redis_funnel.timeit import timeit

with open("get.lua") as script:
    lua = script.read()

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
get = r.register_script(lua)
get = timeit(get)

while True:
    print get(keys=["name"])
