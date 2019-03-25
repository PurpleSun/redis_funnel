#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 21:30
from functools import wraps

from flask import jsonify

from redis_funnel.mgmt.util import Chunk
from redis_funnel.mgmt import error


def api(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            data = f(*args, **kwargs)
            if isinstance(data, dict):
                chunk = Chunk(code=20000, msg=None, data=data).get()
                return jsonify(chunk)
            else:
                return data
        except error.MgmtClientException as e:
            chunk = Chunk(code=e.code, msg=e.msg, data=None).get()
            return jsonify(chunk)
        except Exception as e:
            chunk = Chunk(code=50000, msg=e.message, data=None).get()
            return jsonify(chunk)

    return wrapper
