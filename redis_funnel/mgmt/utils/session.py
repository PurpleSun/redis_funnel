#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/25 12:18
import json
import uuid


class Session(object):
    def __init__(self, redis, expires=3600 * 24, prefix="session"):
        self.redis = redis
        self.expires = expires
        self.prefix = prefix

    @staticmethod
    def _gen_session_id():
        return uuid.uuid4().hex

    def _key(self, session_id):
        return ":".join([self.prefix, session_id])

    def set(self, user):
        session_id = Session._gen_session_id()
        self.redis.set(self._key(session_id), json.dumps(user))
        self.redis.expire(session_id, self.expires)
        return session_id

    def get(self, session_id):
        data = self.redis.get(self._key(session_id))
        if data is None:
            return None
        else:
            return json.loads(data)

    def delete(self, session_id):
        return self.redis.delete(self._key(session_id))
