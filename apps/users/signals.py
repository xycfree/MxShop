#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/3 14:13
# Author: xycfree
# @Descript: 信号量
"""
    pre_save:调用model的save()方法前发送信号
    post_save:调用model的save()方法后发送信号
    pre_delete:调用model活着QuerySets的delete()方法前发送信号
    post_delete：同理，调用delete()后发送信号
    m2m_changed:当一个模型上的ManyToManyField字段被改变的时候发送信号

    链接：https://www.jianshu.com/p/b8cb3d295f8f
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except:
    from users.models import UserProfile as User
log = logging.getLogger(__name__)

# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):

    # 是否新建，因为update的时候也会进行post_save
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()