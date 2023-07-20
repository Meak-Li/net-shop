from django.urls import path,include
from cartapp import views
urlpatterns = [
    path('cartview/',views.cartView),
    path('queryAll/',views.queryAll)
]