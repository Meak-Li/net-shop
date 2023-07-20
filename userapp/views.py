from email.mime import image
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from userapp.models import *
import jsonpickle
from utils.code import gene_text
from django.core import serializers
from utils.cartmanager import *
# Create your views here.
class Register(View):
    """注册视图类"""
    def get(self,request):
        #跳转到注册页面
        return render(request,'userapp/register.html')

    def post(self,request):
        """完成注册"""
        #1.获取表单数据
        uname = request.POST.get('account','')
        pwd = request.POST.get('password','')

        #2.查询数据库是否已经有该用户
        try:
            user = UserInfo.objects.get(uname=uname,pwd=pwd)
            return render(request,'userapp/register.html')
        except UserInfo.DoesNotExist:
            user = UserInfo.objects.create(uname=uname,pwd=pwd)
            #将用户信息存储到session对象
            request.session['user'] = jsonpickle.dumps(user)  #把用户对象序列化为字符串

        return redirect('/userapp/center/') #用户中心

def userCenter(request):
    """用户中心"""
    return render(request,'userapp/center.html')

class LoginView(View):
    """登录视图"""
    def get(self,request):
        #获取请求参数
        reflag = request.GET.get('reflag','')
        #跳转到登录页面
        return render(request,'userapp/login.html',{'reflag':reflag})

    def post(self,request):
        #1.获取请求参数
        uname =request.POST.get('account','')
        pwd = request.POST.get('password','')
        reflag = request.POST.get('reflag','')

        #2.根据输入的账户和密码查询数据是否存在该用户
        user = UserInfo.objects.filter(uname=uname,pwd=pwd)

        #3.如果有该用户，将用户存放到session中，跳转到个人中心页面，如果没有跳转到登录页面
        if user:
            #将用户信息存储到session对象
            request.session['user'] = jsonpickle.dumps(user[0])  #把用户对象序列化为字符串

            #将用户session中购物车数据存储到数据库
            SessionCartManager(request.session).migrateSession2DB()
            if reflag == 'cartapp':
                #从购物车列表跳转到登录页，如果登录成功，跳转到订单列表
                return redirect('/cartapp/queryAll/')
            elif reflag == 'orderapp':
                #获取表单中的参数
                cartitems = request.POST.get('cartitems')
                totalPrice = request.POST.get('totalPrice')
                #从结算页跳转到登录，如果登录成功，跳转到确定订单

                return redirect('/orderapp/toOrder/?cartitems='+cartitems+"&totalPrice="+totalPrice)


            return redirect('/userapp/center/')
        return redirect('/userapp/login/')



def loadCode(request):
    """加载验证码"""
    from captcha.image import ImageCaptcha
    image = ImageCaptcha()
    #获取生成的验证码字符串
    code = gene_text()
    #将code存放到session中
    request.session['session_code'] = code
    imageObj = image.generate(code)
    #返回图片
    return HttpResponse(imageObj,content_type="image/png")

def checkCode(request):
    """校验输入的验证码是否正确"""
    #获取输入的验证码
    code  = request.GET.get('code',-1)
    #获取session对象中验证码
    session_code = request.session.get('session_code',-2)
    #判断是否相等
    vflag = False
    if code == session_code:
        vflag = True
    #返回响应
    return JsonResponse({'vflag':vflag})

def loginout(request):
    """退出登录"""
    #删除session对象及数据库中数据
    request.session.flush()
    #返回响应
    return JsonResponse({'loginout':True})

class AddressView(View):
    """地址管理"""
    def get(self,request):
        #获取当前登录用户
        userinfo = request.session.get('user','')
        if userinfo:
            user = jsonpickle.loads(userinfo)
        #获取当前登录用户关联的收获地址
        addr_list = user.address_set.all()
        return render(request,'userapp/address.html',{'addr_list':addr_list})

    def post(self,request):
        #获取表单数据
        aname = request.POST.get('aname','')
        aphone = request.POST.get('aphone','')
        addr = request.POST.get('addr','')
        #从session中获取当前登录用户
        userinfo = request.session.get('user','')
        if userinfo:
            user = jsonpickle.loads(userinfo)
        #设置是否是默认地址
        #根据当前登录的用户获取地址，查看是否第一个地址
        count = user.address_set.count()
        if count == 0:
            isdefault = True
        else:
            isdefault = False
        #插入数据库
        Address.objects.create(aname=aname,aphone=aphone,addr=addr,userinfo=user,isdefault=isdefault)
        return redirect('/userapp/address/')

def loadArea(request):
    """级联加载地址"""
    pid = request.GET.get('pid',-1)
    #根据pid查询数据
    areaList = Area.objects.filter(parentid=pid)
    #返回响应
    return JsonResponse({'areaList':serializers.serialize('json',areaList)})

def updateDefaultAddrView(request):
    #获取请求参数addrId
    addrId = int(request.GET.get('addrId',-1))

    #修改当前登录用户的默认地址
    #从session中获取当前登录用户
    userinfo = request.session.get('user','')
    if userinfo:
        user = jsonpickle.loads(userinfo)
        #获取当前登录用户所有地址
        addressList = user.address_set.all()
        #循环遍历地址列表
        for address in addressList:
            #设置默认地址
            if address.id == addrId:
                address.isdefault = True
            else:
                address.isdefault = False
            address.save()
        return redirect('/userapp/address/')