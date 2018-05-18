# coding: utf-8
import logging

from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from common.permissions import IsOwnerOrReadOnly
from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer,AddressSerializer

from common.custom_viewset import CreateListDestroyViewSet
User = get_user_model()

log = logging.getLogger(__name__)

class UserFavViewset(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ 用户收藏
        用户收藏数的变化通过信号机制post_save, post_delete控制
        get/post/head/options 加具体参数
        delete方法需要请求具体的goods_id: http://127.0.0.1:8000/userfavs/3/
    """

    # queryset = UserFav.objects.all()
    # serializer_class = UserFavSerializer

    # permission是用来做权限判断的
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # auth使用来做用户认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    # 搜索的字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只能查看当前登录用户的收藏, 不会获取所有用户的收藏
        log.debug("当前登录的用户: {}".format(self.request.user))
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewset(CreateListDestroyViewSet):
    """
        list: 获取用户留言
        create: 添加留言
        delete: 删除留言功能
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """ 收货地址管理
        list:    获取收货地址
        create:  添加收货地址
        update: 更新收货地址
        delete: 删除收货地址
        """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
