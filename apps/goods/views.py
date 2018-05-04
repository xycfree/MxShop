#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/20 10:59
# Author: xycfree
# @Descript:
import logging

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from goods.filter import GoodsFilter
from goods.models import Goods, GoodsCategory, HotSearchWords, Banner
from .serializers import GoodsSerializer, CategorySerializer, HotWordsSerializer, BannerSerializer, \
    IndexCategorySerializer

log = logging.getLogger(__name__)

class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 50


    # def paginate_queryset(self, queryset, request, view=None):
    #     """重写paginate_queryset方法, 主要实现 过滤器在页面中显示"""
    #     pass

    # def get_paginated_response(self, data):
    #     """数据返回格式重写, ==与过滤器冲突=="""
    #     pages = self.page.paginator.count // self.page_size + 1 if \
    #         self.page.paginator.count % self.page_size else self.page.paginator.count//self.page_size
    #     from collections import OrderedDict
    #     return Response(OrderedDict([
    #         ('page_size', self.page_size),
    #         ('count', self.page.paginator.count),
    #         ('page', self.page.number),  # current page
    #         ('next', self.get_next_link()),
    #         ('previous', self.get_previous_link()),
    #         ('data', data),
    #         ('pages', pages)  # pages
    #     ]))


# class GoodsListView(APIView):
#     def get(self, request):
#         goods = Goods.objects.all()[:10]
#
#         serialzer = GoodsSerializer(goods, many=True)
#         return Response(serialzer.data)
#
#     def post(self, request):
#         pass


def index(request):
    log.info("welcome to MxShop")
    return HttpResponse("welcome to MxShop")


class GoodsListView(ListAPIView):
    queryset = Goods.objects.all().order_by("id")
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('category', 'name')
    # def get_queryset(self):
    #     shop_price = self.request.query_params.get('shop_price', 0)
    #     self.queryset = Goods.objects.filter(shop_price__gt=float(shop_price)).order_by('-shop_price')
    #     return self.queryset


class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Goods.objects.all().order_by('-id')  # queryset属性
    """ 不添加排序可能会报以下警告
        UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list: 
        <class 'goods.models.Goods'> QuerySet. paginator = self.django_paginator_class(queryset, page_size)
    """
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 使用过滤器
    filter_class = GoodsFilter
    # filter_fields = ('name',)  # 定义需要过滤的字段, 精确查找
    search_fields = ('name', 'shop_price')  # '^' ：以xx字符串开始搜索 '=' ：完全匹配 '@' ：全文搜索（目前只支持Django的MySQL后端） '$' ：正则表达式搜索

    ordering_fields = ('shop_price',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

        # def get_queryset(self):  # get_queryset方法, 过滤函数, 通过request.query_params.get('shop_price', 0) 接收参数
        #     # shop_price = self.request.query_params.get('shop_price', 0)
        #     # self.queryset = Goods.objects.filter(shop_price__gt=float(shop_price)).order_by('-shop_price')
        #     # return self.queryset
        #     self.queryset = Goods.objects.all().order_by('-id')  # queryset属性
        #     try:
        #         users = UserProfile.objects.get(username=self.request.user)
        #         print("登录的用户: {}".format(users))
        #     except Exception as e:
        #         print(e)
        #         print("用户未登录")
        #     return self.queryset


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ list: 商品分类列表数据   retrieve: 获取商品分类详情 """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 获取热搜词列表 """
    queryset = HotSearchWords.objects.all().order_by("index")
    serializer_class = HotWordsSerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """首页尚品类数据"""
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer