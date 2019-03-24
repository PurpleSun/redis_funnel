#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 10:44
from flask import Flask
from flask import jsonify
import redis

from funnel.mgmt.config import REDIS

app = Flask(__name__)

pool = redis.ConnectionPool(host=REDIS["HOST"], port=REDIS["PORT"], db=REDIS["DB"])
r = redis.Redis(connection_pool=pool)


@app.route("/", methods=["GET"])
def hello():
    rsp = {
        "ping": "pong",
    }
    return jsonify(rsp)


@app.route("/api/group", methods=["GET"])
def get_group_view():
    name = "funnel:groups"
    group_list = list(r.smembers(name))
    group_list.sort()
    rsp = {
        "group_list": group_list,
    }
    return jsonify(rsp)


@app.route("/api/group/<group>", methods=["GET"])
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
    rsp = {
        "funnel_list": funnel_list,
        "total_items": len(funnel_list),
    }
    return jsonify(rsp)


@app.route("/api/key/<key>", methods=["GET"])
def get_key_view(key):
    funnel = r.hgetall(key)
    funnel = {key: float(value) for key, value in funnel.iteritems()}
    funnel["name"] = key
    rsp = {
        "funnel": funnel,
    }
    return jsonify(rsp)


@app.route("/api/key/<key>", methods=["DELETE"])
def delete_key_view(key):
    ret = r.delete(key)
    rsp = {
        "status": ret == 1,
    }
    return jsonify(rsp)


app.run(host="localhost", port=8080, debug=True)
