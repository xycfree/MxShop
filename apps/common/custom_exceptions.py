#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/9 11:15
# Author: xycfree
# @Descript: 自定义异常类

from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback


class Error(Exception):
    def __init__(self, err_code, message='服务器异常', status_code=status.HTTP_400_BAD_REQUEST):
        self.code = err_code
        self.message = message
        self.status_code = status_code

    def __unicode__(self):
        return '[Error] %d: %s(%d)' % (self.code, self.message, self.status_code)

    def get_response(self):
        return error_response(self.code, self.message,  self.status_code)


def error_response(code=status.HTTP_400_BAD_REQUEST, message='failed',
                   status=status.HTTP_400_BAD_REQUEST, headers=None):
    err = {
        'code': code,
        'status_code': status,
        'msg': message,
        'data': [],
    }
    return Response(err, status, headers=headers)


def custom_exception_handler(exc, context):
    # if isinstance(exc, Error):
    #     set_rollback()
    #     return error_response(exc.code,  exc.message, status=exc.status_code)
    #
    # if isinstance(exc, ParseError):
    #     set_rollback()
    #     return error_response(err_code=exc.status_code, message=exc.default_detail, status=exc.status_code)
    #
    # if isinstance(exc, NotFound):
    #     set_rollback()
    #     return error_response(exc.status_code, exc.default_code, exc.default_detail, status=exc.status_code)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    # 调用REST异常处理函数，获得标准的异常响应对象
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    # 为响应对象添加状态码
    if response is not None:
        response.data['code'] = response.status_code
        response.data['data'] = []
        response.data['msg'] = response.data['detail']
        del response.data['detail']
    return response
