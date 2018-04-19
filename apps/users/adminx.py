#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/19 23:08
# @Author  : xycfree
# @Descript:

import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "慕学生鲜后台"
    site_footer = "mxshop"
    # menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)