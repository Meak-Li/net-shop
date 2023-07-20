from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
# Create your views here.
from utils.cartmanager import *
def cartView(request):
    """购物车视图"""
    #在session中存取数据使用多级字典需要实时更新
    request.session.modified = True

    #获取表单数据 
    #1.获取购物操作
    flag = request.POST.get('flag')
    dbCartManageObj = getCartManger(request)
    if flag == 'add':
        """加入购物车"""
        dbCartManageObj.add(**request.POST.dict())
    elif flag == 'plus':
        """增加商品数量"""
        dbCartManageObj.update(step=1,**request.POST.dict())
    elif flag == 'minus':
        dbCartManageObj.update(step=-1,**request.POST.dict())
    elif flag == 'delete':
        dbCartManageObj.delete(**request.POST.dict())

    return redirect('/cartapp/queryAll/') 

def queryAll(request):
    """查询购物车列表"""
    dbCartManageObj = getCartManger(request)
    cartitemList = dbCartManageObj.queryAll()
    print('---',cartitemList)
    return render(request,'cartapp/cart.html',{'cartitemList':cartitemList})







