"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.static import serve
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin
# from goods.views_base import GoodsListView
from MxShop.settings import MEDIA_ROOT
from goods.views import index, GoodsListView, GoodsListViewSet, CategoryViewset, HotSearchsViewset, BannerViewset, IndexCategoryViewset
from rest_framework.routers import DefaultRouter

from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from users.views import UserViewset, SmsCodeViewset
from trade.views import ShoppingCartViewset, OrderViewset

router = DefaultRouter()

# 配置goods的url
router.register(r'goods1', GoodsListViewSet, base_name='goods')
router.register(r'categorys', CategoryViewset, base_name='cagetory')
router.register(r'hotsearchs', HotSearchsViewset, base_name='hotsearch')
router.register(r'banners', BannerViewset, base_name='banner')
router.register(r'indexgoods', IndexCategoryViewset, base_name='index')
router.register(r'users', UserViewset, base_name="users")
router.register(r'sms', SmsCodeViewset, base_name="sms")
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
router.register(r'messages', LeavingMessageViewset, base_name="messages")
router.register(r'address', AddressViewset, base_name="address")
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")
router.register(r'orders', OrderViewset, base_name="orders")


urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api/', include(router.urls, namespace='api')),
    url(r'^index/', index, name='index'),
    url(r'^xadmin/', xadmin.site.urls),
    # url(r'^goods/', GoodsListView.as_view(), name='goods_list')
    url(r'^goods/', GoodsListView.as_view(), name='goods_list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    # url(r'^jwt-auth/', obtain_jwt_token),
    url(r'^login/', obtain_jwt_token),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

]
