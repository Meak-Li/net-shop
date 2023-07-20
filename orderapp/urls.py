from django.urls import path,include
from orderapp import views
urlpatterns = [
    path('toOrder/',views.toOrder),
    path('toPay/',views.toPay),
    path('checkPay/',views.checkPay),
]