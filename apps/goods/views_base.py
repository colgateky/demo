# -*- coding: utf-8 -*-
__author__ = 'mingkun'

from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
import json
from django.forms.models import model_to_dict
from django.core import serializers

from goods.models import Goods


class GoodsListViewDjangoBase(View):
    """
        GoodsListViewDjangoBase
        是以django的view实现商品列表页(最原始的方式)
    """

    def get(self, request):
        # 先定义要返回JSON数据的参数，用於后面装载
        json_list = []
        # 获取所有商品
        goods = Goods.objects.all()
        for good in goods:
            json_dict = {}
            # 获取商品的每个字段，键值对形式
            json_dict['name'] = good.name
            json_dict['category'] = good.category.name
            json_dict['market_price'] = good.market_price
            json_list.append(json_dict)
        # 返回json，一定要指定类型content_type = 'application/json'

        # ensure_ascii是false的时候，可以返回非ASCII码的值，否则就会被JSON转义。
        # 所以含有中文的字典转json字符串时，使用 json.dumps() 方法要把ensure_ascii参数改成false，
        # 即 json.dumps(dict，ensure_ascii = False)，才能显示中文
        content = json.dumps(json_list, ensure_ascii=False)
        response = HttpResponse(content, content_type='application/json', charset='utf-8')
        return response


class GoodsListViewDjangoBase2(View):
    """
        GoodsListViewDjangoBase2是根据上面原始方法再去作更改、简化
        会遇到序列化问题
        1. ImageFieldFile 与 add_time无法序列化，故要使用serializers
    """

    def get(self, request):
        # 通过django的view实现商品列表页
        json_list = []
        # 获取所有商品
        goods = Goods.objects.all()

        json_data = serializers.serialize('json', goods)
        json_data = json.loads(json_data)

        # JsonResponse 与 HttpResponse都能返回json
        # JsonResponse在返回中文的时后会出现unicode编译问题，须加入 json_dumps_params={'ensure_ascii': False} 去生成一个响应
        # HttpResponse则可以指定charset='utf-8'来显示

        response = JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii': False})
        # response = HttpResponse(json_data, content_type='application/json', charset='utf-8')
        return response

    """
    {
        "model": "goods.goods",
        "pk": 1,
        "fields": {
            "category": 20,
            "goods_sn": "",
            "name": "新鲜水果甜蜜香脆单果约800克",
            "click_num": 0,
            "sold_num": 0,
            "fav_num": 0,
            "goods_num": 0,
            "market_price": 232.0,
            "shop_price": 156.0,
            "goods_brief": "食用百香果可以增加胃部饱腹感，减少余热量的摄入，还可以吸附胆固醇和胆汁之类有机分子，抑制人体对脂肪的吸收。因此，长期食用有利于改善人体营养吸收结构，降低体内脂肪，塑造健康优美体态。",
            "goods_desc": "<p><img src=\"/media/goods/images/2_20170719161405_249.jpg\" title=\"\" alt=\"2.jpg\"/></p><p><img src=\"/media/goods/images/2_20170719161414_628.jpg\" title=\"\" alt=\"2.jpg\"/></p><p><img src=\"/media/goods/images/2_20170719161435_381.jpg\" title=\"\" alt=\"2.jpg\"/></p>",
            "ship_free": true,
            "goods_front_image": "goods/images/1_P_1449024889889.jpg",
            "is_new": false,
            "is_hot": false,
            "add_time": "2019-08-13T15:07:58.825"
            }
    }
    上面是返回的JSON字段
    django的serializer虽然可以很简单实现序列化，但是有几个缺点
    1. 字段序列化定死的，要想重组的话非常麻烦
    2. images保存的是一个相对路径，我们还需要补全路径，而这些drf都可以帮助我们做到
    
    """
