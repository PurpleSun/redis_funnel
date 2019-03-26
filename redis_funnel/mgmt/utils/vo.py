#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 21:28


class Chunk(object):
    def __init__(self, code=None, msg=None, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    def set_code(self, code):
        self.code = code
        return self

    def set_msg(self, msg):
        self.msg = msg
        return self

    def set_data(self, data):
        self.data = data
        return self

    def get(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data,
        }
