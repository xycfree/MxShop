#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/20 10:59
# Author: xycfree
# @Descript:

import logging
from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets, authentication, permissions, status
from rest_framework.mixins import CreateModelMixin
# Create your views here.
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from users.models import VerifyCode
from users.serializers import UserRegSerializer, UserDetailSerializer, SmsSerializer

User = get_user_model()

log = logging.getLogger(__name__)

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因
            # 后期可以添加邮箱验证
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """发送短信验证码"""
    serializer_class = SmsSerializer

    def generate_code(self):
        """生成四位数字验证码"""
        seeds = ''.join([str(i) for i in range(10)])
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        log.info('serializer: {}'.format(serializer))
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        code = self.generate_code()
        log.info("mobile: {}, code: {}".format(mobile, code))
        try:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({"mobile": mobile, 'msg': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            log.exception(e)
            return Response({"mobile": mobile, 'msg': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
        """
        短信发送验证，
        yun_pian = YunPian(APIKEY)
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)
        if sms_status["code"] != 0:
            return Response({
                "mobile":sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            }, status=status.HTTP_201_CREATED)
        """



class UserViewset(CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """用户信息"""
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        """ 这里需要动态选择用哪个序列化方式
            UserRegSerializer（用户注册），只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
            问题又来了，如果注册的使用userdetailSerializer，又会导致验证失败，所以需要动态的使用serializer
        """
        if self.action == 'retrieve':
            log.debug("获取用户详情...")
            return UserDetailSerializer
        elif self.action == 'create':
            log.debug("注册新用户...")
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """ 这里需要动态权限配置
            #1.用户注册的时候不应该有权限限制
            #2.当想获取用户详情信息的时候，必须登录才行
        """
        log.debug('验证用户权限...')
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        log.debug("users create serializer: {}".format(serializer))
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        log.debug("users create re_dict: {}".format(re_dict))

        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        """#虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
        #重写get_object方法，就知道是哪个用户了"""
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

"""
    继承mixins.RetrieveModelMixin   -->>获取用户信息
    重写get_object                              -->>获取登录的用户
    get_permissions                           -->>动态权限分配
    get_serializer_class                     -->>动态序列化分配
"""