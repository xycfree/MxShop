# coding: utf-8
import logging

from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav
from user_operation.serializers import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly

User = get_user_model()

log = logging.getLogger(__name__)

class UserFavViewset(mixins.ListModelMixin,mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ 用户收藏
        用户收藏数的变化通过信号机制post_save, post_delete控制
        get/post/head/options 加具体参数
        delete方法需要请求具体的goods_id: http://127.0.0.1:8000/userfavs/3/
    """

    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

    # permission是用来做权限判断的
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # auth使用来做用户认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 搜索额字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只能查看当前登录用户的收藏, 不会获取所有用户的收藏
        log.debug("当前登录的用户: {}".format(self.request.user))
        return UserFav.objects.filter(user=self.request.user)
