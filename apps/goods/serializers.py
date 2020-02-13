from rest_framework import serializers

from goods.models import Goods, GoodsCategory


# APIView所使用的最基础serializers
# Serializer应用在每个参数每个参数去做定义，以下假设用三个参数
# 这边指定几个参数就会有几个
class GoodsSerializerBasic(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    click_num = serializers.IntegerField(default=0)
    goods_front_image = serializers.ImageField()


# ModelSerializer更高级点
# ModelSerializer 就是直接用model.py的内容去建立，藉由指定model = Goods去对应

class CategorySerializerLevel3(serializers.ModelSerializer):
    """
    三级分类
    """
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializerLevel2(serializers.ModelSerializer):
    """
    二级分类
    """
    # 在parent_category字段中定义的related_name="sub_cat"
    # many=True 代表资料有多笔，如果不这样会报错
    sub_cat = CategorySerializerLevel3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    商品一级类别序列化
    """
    sub_cat = CategorySerializerLevel2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    # 如果内层有再包装，可以再写在用另一个serializer再去获取
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = '__all__'
