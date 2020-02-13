import django_filters
from django.db.models import Q

from goods.models import Goods


class GoodsFilterBase(django_filters.rest_framework.FilterSet):
    """
    自定义商品过滤类
    """
    # 两个参数，field_name是要过滤的参数，lookup是执行的行为
    # Goods.objects.filter(shop_price__gte=) 等同于下面的lookup_expr='gte'
    # 大於等於 与 小於等於本店价格
    price_min = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']


class GoodsFilterToVue(django_filters.rest_framework.FilterSet):
    """
    自定义商品过滤类
    """
    # 两个参数，field_name是要过滤的参数，lookup是执行的行为
    # 大於等於 与 小於等於本店价格
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        # 不管当前点击的是一级分类/二级分类/三级分类，后面都能找到
        filter_condition = \
            Q(category_id=value) | Q(category__parent_category_id=value) \
            | Q(category__parent_category__parent_category_id=value)
        filter_result = queryset.filter(filter_condition)
        return filter_result

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax']
