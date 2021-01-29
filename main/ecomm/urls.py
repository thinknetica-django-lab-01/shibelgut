from django.urls import path
from .views import index
from ecomm.views import GoodsList, GoodsDetail


urlpatterns = [
    path('', index, name='main_url'),
    path('goods/', GoodsList.as_view(), name='goods_list_url'),
    path('goods/<int:pk>/', GoodsDetail.as_view(), name='goods_detail_url'),
]
