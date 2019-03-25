#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: fanwei.zeng
# Time: 2019/3/25 09:32


class RedisFunnelException(Exception):
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = msg


class MgmtClientException(RedisFunnelException):
    pass


class MgmtServerException(RedisFunnelException):
    pass


USERNAME_PASSWORD_ABSENCE_ERROR = MgmtClientException(40001, u"argument username or password absence")
INVALID_USERNAME_ERROR = MgmtClientException(40002, u"invalid username")
INVALID_PASSWORD_ERROR = MgmtClientException(40002, u"invalid password")
NOT_LOGIN_ERROR = MgmtClientException(40003, u"login need")
SESSION_EXPIRED_ERROR = MgmtClientException(40004, u"session expired")
