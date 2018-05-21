#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/18 15:39
# Author: xycfree
# @Descript: 自定义视图集

from rest_framework import mixins, viewsets


class CreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """ 显示列表，详情, 创建
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    pass


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
        A viewset that provides `destroy`, `create`, and `list` actions.

        To use it, override the class and set the `.queryset` and
        `.serializer_class` attributes.
        """
    pass