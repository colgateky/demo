from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from goods.filters import GoodsFilterBase, GoodsFilterToVue
from goods.models import Goods, GoodsCategory
from goods.serializers import GoodsSerializer, CategorySerializer, GoodsSerializerBasic


class GoodsPagination(PageNumberPagination):
    """
        商品列表自定义分页
    """
    # 每页显示的个数(需适应前端页面上的每页显示数量)
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = "page"
    # 最多能显示多少页
    max_page_size = 10000


# 使用APIView方式去获取
class GoodListView(APIView):
    """
    List all Goods
    """

    def get(self, request, format=None):
        goods = Goods.objects.all()
        serializer = GoodsSerializerBasic(goods, many=True)
        return Response(serializer.data)


# GenericAPIView继承APIView，封装了很多方法，比APIView功能更强大
# class GoodsListView(generics.ListAPIView)取代，那下面的def get就不用写了
class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
    """商品列表页"""
    # 引用GenericAPIView，需定义queryset与serializer_class
    # 因为在GenericAPIView这里面两个参数为空
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    # 一定要重写get, post, delete方法，不然系统会默认不接受get, post, delete方法
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# 比GenericAPIView更进阶的ViewSet
class GoodsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    商品列表页, 分页， 搜索， 过滤， 排序
    """
    queryset = Goods.objects.all()
    # 分页
    pagination_class = GoodsPagination
    # 序列化
    serializer_class = GoodsSerializer

    # Token Auth验证
    # authentication_classes = (TokenAuthentication, )

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    # 设置filter对应到我们自定义的类
    # 过滤
    filter_class = GoodsFilterToVue
    # 添加搜索功能，这边使用馍糊搜寻，搜寻下面三个参数中具有该字段即输出 (=name则表示精确搜索)
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 添加排序功能
    # 这部份要与前端一致
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
