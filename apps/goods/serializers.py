#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/20 11:28
# Author: xycfree
# @Descript:
from django.db.models import Q
from rest_framework import serializers

from .models import Goods, GoodsCategory, HotSearchWords, GoodsCategoryBrand, IndexAd


# class GoodsSerializer(serializers.Serializer):
#     """继承serializers.Serializer, 自定义生成字段"""
#     name = serializers.CharField(required=True, max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)

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


class HotWordsSerializer(serializers.ModelSerializer):
    """热搜词Model生成字段"""

    class Meta:
        model = HotSearchWords
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(goods_ins, many=False, context={'request': self.context})
        return goods_json

    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"
