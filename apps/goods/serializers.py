#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/20 11:28
# Author: xycfree
# @Descript:

from rest_framework import serializers

from .models import Goods, GoodsCategory


# class GoodsSerializer(serializers.Serializer):
#     """继承serializers.Serializer, 自定义生成字段"""
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()



class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    """基于数据库Model生成字段"""
    category = CategorySerializer()
    class Meta:
        model = Goods
        # 显示的字段, category_id为外键，直接显示的是id值，如需显示全部内容，需要对Serializer嵌套使用覆盖外键字段
        # fields = ('name', 'click_num', 'goods_front_image', 'add_time', 'category')
        fields = '__all__'  # 显示所有字段




