#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/24 10:44
import time
from functools import wraps

from flask import Flask, request, make_response, jsonify
import redis

from redis_funnel.mgmt.config import REDIS, ACCOUNTS, SESSION_EXPIRES
from redis_funnel.mgmt.utils import error
from redis_funnel.mgmt.utils.session import Session
from redis_funnel.mgmt.utils.decorator import api
from redis_funnel.mgmt.utils.vo import Chunk
from redis_funnel.mgmt.utils import code


app = Flask(__name__)

pool = redis.ConnectionPool(host=REDIS["HOST"], port=REDIS["PORT"], db=REDIS["DB"])
r = redis.Redis(connection_pool=pool)
session = Session(r, expires=SESSION_EXPIRES)
SESSION_ID = "session_id"


def auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        session_id = request.cookies.get(SESSION_ID)
        if session_id is None:
            raise error.NOT_LOGIN_ERROR

        user = session.get(session_id)
        if user is None:
            raise error.SESSION_EXPIRED_ERROR

        request.user = user
        return f(*args, **kwargs)

    return wrapper


@app.route("/", methods=["GET"])
@api
def index():
    data = {
        "ping": "pong",
    }
    return data


@app.route("/login", methods=["POST"])
@api
def login():
    session_id = request.cookies.get(SESSION_ID)
    if session_id is not None:
        user = session.get(session_id)
        if user is not None:
            return {
                "user": user
            }

    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:
        raise error.USERNAME_PASSWORD_ABSENCE_ERROR
    if username not in ACCOUNTS:
        raise error.INVALID_USERNAME_ERROR
    if password != ACCOUNTS.get(username):
        raise error.INVALID_PASSWORD_ERROR

    user = {
        "username": username,
        "login_ts": time.time()
    }
    session_id = session.set(user)
    data = {
        "user": user
    }
    chunk = Chunk(code=code.OK, msg=None, data=data).get()
    res = make_response(jsonify(chunk))
    res.set_cookie(SESSION_ID, session_id, max_age=SESSION_EXPIRES, httponly=True)
    return res


@app.route("/logout", methods=["GET"])
@api
def logout():
    session_id = request.cookies.get(SESSION_ID)
    cnt = None
    if session_id is not None:
        cnt = session.delete(session_id)

    data = {
        "success": cnt == 1
    }
    return data


@app.route("/api/group", methods=["GET"])
@api
@auth
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
@auth
def get_group_keys_view(group):
    name = "funnel:" + group + ":keys"
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
@auth
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
@auth
def delete_key_view(key):
    ret = r.delete(key)
    data = {
        "status": ret == 1,
    }
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
