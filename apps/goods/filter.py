#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/25 16:44
# Author: xycfree
# @Descript:

import django_filters

from goods.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """自定义过滤类"""
    name = django_filters.CharFilter(name='name', lookup_expr='icontains')
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['name', 'price_min', 'price_max']
        # ording = ('-shop_price', )