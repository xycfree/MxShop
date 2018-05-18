#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/4 18:18
# Author: xycfree
# @Descript:

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     """针对每一次请求的权限检查"""
    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    def has_object_permission(self, request, view, obj):
        """针对数据库条目的权限检查，返回 True 表示允许"""
        # 允许访问只读方法
        if request.method in permissions.SAFE_METHODS:
            return True

        # 非安全方法需要检查用户是否是 owner
        return obj.user == request.user