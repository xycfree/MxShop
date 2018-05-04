#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/3 10:52
# Author: xycfree
# @Descript:
import logging
import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import VerifyCode
from MxShop.settings import REGEX_MOBILE

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except:
    from users.models import UserProfile as User

log = logging.getLogger(__name__)

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        # 函数名必须：validate + 验证字段名
        log.info("验证码手机号合法性...")
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已注册")

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile

    # class Meta:
    #     model = VerifyCode
    #     fields = ("mobile", 'code')



class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化"""
    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")

class UserRegSerializer(serializers.ModelSerializer):
    """用户注册序列化"""
    code = serializers.CharField(required=True, write_only=True, max_length=6, min_length=4, label='验证码',
                                 error_messages={
                                     'blank': '请输入验证码',
                                     'required': '请输入验证码',
                                     'max_length': '验证码格式错误',
                                     'min_length': '验证码格式错误',
                                 },
                                 help_text='验证码')
    username = serializers.CharField(label='用户名', help_text='用户名[手机号]', required=True, allow_blank=False,
                                     validators=[UniqueValidator(User.objects.all(), message='该用户已注册')])
    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码', label='密码', write_only=True)

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        # 函数名必须：validate + 验证字段名
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        # 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")

