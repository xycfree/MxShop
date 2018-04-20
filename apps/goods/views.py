#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018/4/20 10:59
# Author: xycfree
# @Descript:
from rest_framework import request, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from goods.models import Goods
from .serializers import GoodsSerializer
from django_filters.rest_framework import DjangoFilterBackend

class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 50

    def get_paginated_response(self, data):
        from collections import OrderedDict
        return Response(OrderedDict([
            ('count', self.page.paginator.count),  # count
            ('page', self.page.number),  # current page
            ('next', self.get_next_link()),  # next link
            ('previous', self.get_previous_link()),  # previous link
            ('data', data),  # data
            ('pages', self.page.paginator.count // self.page_size + 1 if \
            self.page.paginator.count % self.page_size else self.page.paginator.count//self.page_size)  # pages
        ]))
        # code ('code', 'C00000' if data else 'C00002')
        # msg ('msg', 'success' if data else 'failed')



# class GoodsListView(APIView):
#     def get(self, request):
#         goods = Goods.objects.all()[:10]
#
#         serialzer = GoodsSerializer(goods, many=True)
#         return Response(serialzer.data)
#
#     def post(self, request):
#         pass



class GoodsListView(ListAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    def get_queryset(self):
        shop_price = self.request.query_params.get('shop_price', 0)
        self.queryset = Goods.objects.filter(shop_price__gt=float(shop_price)).order_by('-shop_price')
        return self.queryset


class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    filter_backends = (DjangoFilterBackend,)



    def get_queryset(self):
        shop_price = self.request.query_params.get('shop_price', 0)
        self.queryset = Goods.objects.filter(shop_price__gt=float(shop_price)).order_by('-shop_price')
        return self.queryset