from decimal import MAX_EMAX
from django.http import HttpResponse
from django.shortcuts import render
from goodsapp.models import *
from django.core.paginator import Paginator
from netshop import settings
# Create your views here.
# 新增 1 2 3 4 5 6 7 8 这样的分页栏函数
def get_page_range_by_page_and_max_page(page, max_page, num=10):
    min = page-int(num/2)
    min = min if min > 1 else 1
    max = min + num - 1
    max = max if max < max_page else max_page

    return range(min, max + 1)
def index(request,categoryid=2,page_num = 1):
    """商品列表页"""
    #1.获取所有分类
    categoryList = Category.objects.all().order_by('id')

    #2.获取当前分类下的所有商品
    goodsList = Goods.objects.filter(category_id = categoryid).order_by('id')

    #添加分页
    paginator = Paginator(object_list=goodsList,per_page=settings.PER_PAGE_NUMBER)
    #获取当前page_num页的数据
    goods_page = paginator.get_page(page_num)


    #设置传递参数
    context = {
        'categoryList':categoryList,
        'currcategoryid':categoryid,
        'goods_page':goods_page,
        'page_range':get_page_range_by_page_and_max_page(page_num,paginator.num_pages) #第一参数当前页，第二参数总共多少页
        }
    return render(request,'goodsapp/index.html',context=context)

def recommend(func):
    def inner(request,goodsid,*args,**kwargs):
        #浏览商品id ,从cookie中获取浏览商品id  (由空格拼接的字符串)
        c_goodsIdList = request.COOKIES.get('recommend_goodsid','')

        #将由空格拼接的字符串 转换为列表
        goodsIdList = [id for id in c_goodsIdList.split() if id.strip()]

        #先判断当前浏览的商品是否在浏览列表中，如果存在先删除，再将商品插入列表第一位置
        if str(goodsid) in goodsIdList:
            goodsIdList.remove(str(goodsid))
        goodsIdList.insert(0,goodsid)

        #根据推荐商品id获取商品信息
        goodsObjectsList = [Goods.objects.get(id=gid) for gid in goodsIdList if gid!=goodsid and Goods.objects.get(id=gid).category.id == Goods.objects.get(id=goodsid).category.id][:4]

        #使用COOKIE保存浏览商品id
        #获取resonse
        response = func(request,goodsid,recommend_list=goodsObjectsList,*args,**kwargs)

        #获取cookie
        response.set_cookie('recommend_goodsid',' '.join([str(id) for id in goodsIdList]),max_age=3*24*3600)
        return response
    return inner


@recommend
def goodsdetail(request,goodsid,recommend_list=[]):
    """根据商品id获取商品详情"""
    try:
        #根据商品id获取商品
        goods = Goods.objects.get(id=goodsid)
        return render(request,'goodsapp/goodsdetail.html',{'goods':goods,'recommend_list':recommend_list})
    except Goods.DoesNotExist:
        return HttpResponse(status=404)