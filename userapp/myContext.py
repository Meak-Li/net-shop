import jsonpickle


def getUserInfo(request):
    """获取用户对象信息"""
    #从session对象获取用户  该用户是字符串
    user = request.session.get('user')

    #将字符串 返序列化为对象
    if user:
        user = jsonpickle.loads(user)
    return {'userInfo':user}