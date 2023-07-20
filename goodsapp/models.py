from distutils.command.upload import upload
from pyexpat import model
from unicodedata import category
from django.db import models

# Create your models here.
class Category(models.Model):
    """商品分类"""
    cname = models.CharField(max_length=10,verbose_name='商品分类名称')

    def __str__(self) -> str:
        return self.cname

class Goods(models.Model):
    """商品表"""
    gname = models.CharField(max_length=100,verbose_name="商品名称")
    gdesc = models.CharField(max_length=100,verbose_name='商品描述')
    oldprice = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='商品原价')
    price = models.DecimalField(max_digits=5,decimal_places=2,verbose_name='商品现价')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    #获取商品图片
    def getImgUrl(self):
        return self.inventory_set.first().color.colorurl

    #获取颜色
    def getColors(self):
        colors = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            #去掉重复的
            if color not in colors:
                colors.append(color)
        return colors

    #获取尺码
    def getSizes(self):
        sizes = set()
        for inventory in self.inventory_set.all():
            sizes.add(inventory.size)
        return sizes

    #存储结构：{'参数规格':['url'],'整体款式':['url'],'模特实拍':['url1','url2','url3'...]}
    def getDetailInfo(self):
        #存储数据
        datas = {}
        #根据商品获取商品详情
        for detail in self.goodsdetail_set.all():
            #根据商品详情获取商品详情名称
            detailName = detail.detailname.gdname
            #判断字典数据中是否已经有key为detailName
            if detailName in datas:
                datas[detailName].append(detail.gdurl)
            else:
                datas[detailName] = [detail.gdurl]

        return datas


    def __str__(self) -> str:
        return self.gname

class GoodsDetailName(models.Model):
    """商品详细名称表"""
    gdname = models.CharField(max_length=30,verbose_name='商品详细名称')

    def __str__(self) -> str:
        return self.gdname

class GoodsDetail(models.Model):
    """商品详细表"""
    gdurl = models.ImageField(verbose_name='详细图片路径',upload_to='')
    detailname = models.ForeignKey(GoodsDetailName,on_delete=models.CASCADE,verbose_name='商品详细名称')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

class Size(models.Model):
    """商品尺寸"""
    sname = models.CharField(verbose_name='商品尺寸名称',max_length=10)

class Color(models.Model):
    """商品颜色"""
    colorname = models.CharField(max_length=10,verbose_name="颜色名称")
    colorurl = models.ImageField(verbose_name="颜色保存路径",upload_to='color/')

class Inventory(models.Model):
    """商品库存"""
    count = models.PositiveBigIntegerField(verbose_name='库存数量')
    size = models.ForeignKey(Size,on_delete=models.CASCADE,verbose_name="所数尺寸")
    color = models.ForeignKey(Color,on_delete=models.CASCADE,verbose_name='所属颜色')
    goods = models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name='所属商品')