"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

import xadmin

from demo.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from goods.views import GoodsListViewSet, CategoryViewSet, GoodListView
from goods.views_base import GoodsListViewDjangoBase, GoodsListViewDjangoBase2

# ViewSet与Router配套使用
router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置category的url
router.register(r'categorys', CategoryViewSet, base_name='categorys')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),

    # 商品列表页
    # url(r'goods/$', GoodsListViewDjangoBase2.as_view(), name='goods-list'),  # 原始写法
    # url(r'goods/$', GoodListView.as_view(), name='goods-list'),  # 用drf方式，
    url(r'^', include(router.urls)),

    # drf文档，title自定义
    url(r'docs/', include_docs_urls(title='Django + Vue生鲜的drf文档')),

    url(r'^api-token-auth/', views.obtain_auth_token)  # 获取token的url配置
]
