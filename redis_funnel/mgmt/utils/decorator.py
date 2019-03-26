#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 21:30
from functools import wraps

from flask import jsonify

from redis_funnel.mgmt.utils.vo import Chunk
from redis_funnel.mgmt.utils import error
from redis_funnel.mgmt.utils import code


def api(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            data = f(*args, **kwargs)
            if isinstance(data, dict):
                chunk = Chunk(code=code.OK, msg=None, data=data).get()
                return jsonify(chunk)
            else:
                return data
        except error.MgmtClientException as e:
            chunk = Chunk(code=e.code, msg=e.msg, data=None).get()
            return jsonify(chunk)
        except error.MgmtServerException as e:
            chunk = Chunk(code=e.code, msg=e.msg, data=None).get()
            return jsonify(chunk)
        except Exception as e:
            chunk = Chunk(code=code.SERVER_ERROR, msg=e.message, data=None).get()
            return jsonify(chunk)

    return wrapper
