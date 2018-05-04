#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/4 18:45
# Author: xycfree
# @Descript:

from user_operation.models import UserFav
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    if goods.fav_num < 0:
        goods.fav_num = 0
    goods.save()
