#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 11:26

# redis config
REDIS = {
    "HOST": "localhost",
    "PORT": 6379,
    "DB": 0,
}

# key as username, and value as password
ACCOUNTS = {
    "admin": "admin",
}

# session expire time, in second unit
SESSION_EXPIRES = 3600 * 24
