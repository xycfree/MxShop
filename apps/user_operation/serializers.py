#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/4 17:52
# Author: xycfree
# @Descript:

from rest_framework import serializers

from goods.serializers import GoodsSerializer
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from rest_framework.validators import UniqueTogetherValidator


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):

    # 获取当前登录的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏',
            )
        ]
        model = UserFav

        fields = ('user', 'goods', 'id')  # 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少


class LeavingMessageSerializer(serializers.ModelSerializer):
    """用户留言"""

    # 获取当前登录的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        # fields = ("user", "message_type", "subject", "file", "id", "add_time")
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserAddress
        fields = "__all__"