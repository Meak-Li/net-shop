from django.urls import path,include
from goodsapp import views
urlpatterns = [
    path('',views.index), #商品列表
    path('category/<int:categoryid>/page/<int:page_num>/',views.index),#根据分类和分类
    path('category/<int:categoryid>/',views.index),#根据分类查询
    path('goodsdetails/<int:goodsid>/',views.goodsdetail)
]