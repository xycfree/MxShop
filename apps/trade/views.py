from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from common.custom_viewset import CreateListRetrieveViewSet
from common.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from .serializers import ShopCartSerializer, OrderSerializer, OrderDetailSerializer
from .models import ShoppingCart, OrderInfo, OrderGoods


class ShoppingCartViewset(viewsets.ModelViewSet):
    """ 购物车功能
        list: 购物车列表
        retrieve: 购物车详情
        create: 加入购物车
        delete: 删除购物车记录
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = ShopCartSerializer
    lookup_field = 'goods_id'  # 搜索关键词

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

class OrderViewset(CreateListRetrieveViewSet):
    """ 订单管理
        list: 获取个人订单
        retrieve: 订单详情
        crete: 新增订单
        delete: 删除订单
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        """获取订单列表"""
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save()

        # 获取购物车锁商品
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order

            shop_cart.delete()  # 清空购物车
        return order