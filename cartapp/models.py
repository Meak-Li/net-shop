from turtle import color
from django.db import models
from userapp.models import UserInfo 
from goodsapp.models import *

# Create your models here.
class CartItem(models.Model):
    """购物车"""
    goodsid = models.PositiveIntegerField(verbose_name="商品id")
    colorid = models.PositiveIntegerField(verbose_name="颜色id")
    sizeid = models.PositiveIntegerField(verbose_name="尺寸id")
    count = models.PositiveIntegerField(default=0,verbose_name="商品数量")
    isdelete = models.BooleanField(default=False,verbose_name="是否删除")
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE,verbose_name="用户")

    def __str__(self) -> str:
        return str(self.count)

    def getColor(self):
        return Color.objects.get(id=self.colorid)

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getSize(self):
        return Size.objects.get(id=self.sizeid)

    def getTotalPrice(self):
        return int(self.getGoods().price)*int(self.count)