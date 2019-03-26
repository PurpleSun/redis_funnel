#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/25 09:32
from redis_funnel.mgmt.utils.code import CLIENT_ERROR


class RedisFunnelException(Exception):
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = msg


class MgmtClientException(RedisFunnelException):
    pass


class MgmtServerException(RedisFunnelException):
    pass


USERNAME_PASSWORD_ABSENCE_ERROR = MgmtClientException(CLIENT_ERROR + 1, u"argument username or password absence")
INVALID_USERNAME_ERROR = MgmtClientException(CLIENT_ERROR + 2, u"invalid username")
INVALID_PASSWORD_ERROR = MgmtClientException(CLIENT_ERROR + 3, u"invalid password")
NOT_LOGIN_ERROR = MgmtClientException(CLIENT_ERROR + 4, u"not login yet")
SESSION_EXPIRED_ERROR = MgmtClientException(CLIENT_ERROR + 5, u"session expired")
