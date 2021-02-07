from django.urls import path
from .views import index
from ecomm.views import GoodsListView, GoodsDetailView, ProfileUserUpdate


urlpatterns = [
    path('', index, name='main_url'),
    path('goods/', GoodsListView.as_view(), name='goods_list_url'),
    path('goods/<int:pk>/', GoodsDetailView.as_view(), name='goods_detail_url'),
    path('accounts/profile/', ProfileUserUpdate.as_view(), name='profile_user_update_url'),
]
