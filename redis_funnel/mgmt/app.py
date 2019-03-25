#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 10:44
from flask import Flask
import redis

from redis_funnel.mgmt.config import REDIS
from redis_funnel.mgmt.decorator import api


app = Flask(__name__)

pool = redis.ConnectionPool(host=REDIS["HOST"], port=REDIS["PORT"], db=REDIS["DB"])
r = redis.Redis(connection_pool=pool)


@app.route("/", methods=["GET"])
@api
def hello():
    data = {
        "ping": "pong",
    }
    return data


@app.route("/api/group", methods=["GET"])
@api
def get_group_view():
    name = "funnel:groups"
    group_list = list(r.smembers(name))
    group_list.sort()
    data = {
        "group_list": group_list,
    }
    return data


@app.route("/api/group/<group>", methods=["GET"])
@api
def get_group_keys_view(group):
    name = 'funnel:' + group + ':keys'
    key_members = r.smembers(name)
    funnel_list = []
    for key in key_members:
        funnel = r.hgetall(key)
        funnel = {key: float(value) for key, value in funnel.iteritems()}
        funnel["name"] = key
        funnel_list.append(funnel)
    funnel_list.sort(key=lambda x: x["name"])
    data = {
        "funnel_list": funnel_list,
        "total_items": len(funnel_list),
    }
    return data


@app.route("/api/key/<key>", methods=["GET"])
@api
def get_key_view(key):
    funnel = r.hgetall(key)
    funnel = {key: float(value) for key, value in funnel.iteritems()}
    funnel["name"] = key
    data = {
        "funnel": funnel,
    }
    return data


@app.route("/api/key/<key>", methods=["DELETE"])
@api
def delete_key_view(key):
    ret = r.delete(key)
    data = {
        "status": ret == 1,
    }
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
