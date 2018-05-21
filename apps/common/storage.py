#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/5/21 9:26
# Author: xycfree
# @Descript: 上传文件重命名-uuid4

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


class FilesStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(FilesStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        """
        :param name: 上传的文件名
        :param content: 内容
        :return:
        """
        """重写 _save方法"""
        import os, time, random
        import uuid
        ext = os.path.splitext(name)[1]  # 获取文件扩展名
        _dir = os.path.dirname(name)  # 文件目录
        # fn = time.strftime('%y%m%d%H%M%S')
        # fn = fn + '_%d' % random.randint(0, 100)
        fn = uuid.uuid4().__str__()  # uuid4
        name = os.path.join(_dir, fn + ext)  # 文件重命名

        return super(FilesStorage, self)._save(name, content)