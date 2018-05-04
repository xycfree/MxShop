#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/4 17:52
# Author: xycfree
# @Descript:

from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator


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
