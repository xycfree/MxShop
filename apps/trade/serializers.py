#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/21 11:21
# Author: xycfree
# @Descript:
from goods.serializers import GoodsSerializer
from .models import ShoppingCart, OrderGoods, OrderInfo
from goods.models import Goods
from rest_framework import serializers


class ShopCartSerializer(serializers.Serializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # 获取当前挡路用户

    nums = serializers.IntegerField(required=True, label='数量', min_value=1,
                                    error_messages={
                                        'min_value': '商品数量不能小于一',
                                        'required': '请选择购买数量',
                                    })
    # 这里是集成Serializer, 必须指定queryset, 如果指定ModelSerializer则不需要指定
    # goods是外键，可以通过这方法获取goods object中所有的值
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    # 继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):

        # validated_data是已经处理过的数据
        # 获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        # 如果购物车中有记录，数量+1;  如果购物车车没有记录，就创建
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)  # 添加到购物车
        return existed

    # 继承Serializer，需要重写实现update, 承modelSerializer，不需要实现update
    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单中的商品"""
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单商品信息"""
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # 生成订单时不用post
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    nonce_str = serializers.CharField(read_only=True)
    pay_type = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        """生成订单号 当前时间+userid+随机数"""
        import time
        from random import randint

        order_sn = "{}{}{}".format(time.strftime('%Y%m%d%H%M%S'),
                                   self.context['request'].user.id,
                                   randint(1, 99))
        return order_sn

    def validate(self, attrs):
        # validate中添加order_sn，然后在view中就可以save
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
