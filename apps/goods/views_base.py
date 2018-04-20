# coding: utf-8
import json

from django.core import serializers
from django.http import JsonResponse
from django.views import View

from goods.models import Goods


class GoodsListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:10]
        # goods = [model_to_dict(di) for di in goods]
        # return HttpResponse(json.dumps(goods, ensure_ascii=False, indent=2))  # 不能解析图片和时间
        json_data = serializers.serialize('json', goods)  # 序列化
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)

    def post(self, request):
        pass
