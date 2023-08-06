import re
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from mengling_tool.database_tool2.__sqltool__ import encryption, decrypt


def runGetFunc(request: WSGIRequest, getfunc, *keys):
    if request.method != 'GET' or len(request.GET.keys()) != len(keys): return None
    values = list()
    for key in keys:
        value = request.GET.get(key, None)
        if value is None:
            return None
        else:
            values.append(value)
    return getfunc(request, *values)


def runPostFunc(request: WSGIRequest, postfunc, *keys):
    if request.method != 'POST' or len(request.POST.keys()) != len(keys): return None
    values = list()
    for key in keys:
        value = request.POST.get(key, None)
        if value is None:
            return None
        else:
            values.append(value)
    return postfunc(request, *values)


# 注册界面
def register_func(sqltool, user_table):
    def temp(func):
        def refunc(request: WSGIRequest):
            def register_post(rt, name, tid, password):
                password = encryption(tid, password)
                # 防止sql注入
                if re.match('^\w+$', tid) is None:
                    result = render(rt, '登录注册/注册.html', {'note': '账号名有误!'})
                elif sqltool.ifGet(user_table, where=f"tid='{tid}'"):
                    result = render(rt, '登录注册/注册.html', {'note': f'账号名{tid}已存在!'})
                else:
                    try:
                        sqltool.insert(user_table, ['name', 'tid', 'password'], [name, tid, password])
                        sqltool.commit()
                        print(name, tid, password, '注册成功')
                        result = HttpResponse(f'alert("注册成功!");window.location.href="/login/";')
                    except:
                        sqltool.rollback()
                        result = HttpResponse('alert("插入数据库出错,请联系管理员-梦灵");')
                return result

            get = runGetFunc(request, lambda request: render(request, '登录注册/注册.html'))
            post = runPostFunc(request, register_post, 'name', 'tid', 'password')
            func(request, sqltool)
            if get is not None:
                return get
            elif post is not None:
                return post
            else:
                raise Http404()

        return refunc

    return temp


# 退出登录
def exit(request: WSGIRequest):
    try:
        request.session.clear()
    except:
        pass
    return redirect('/login/')


# 登录界面
def login_func(sqltool, user_table,name_lie='tid',pwd_lie='password'):
    def temp(func):
        def refunc(request: WSGIRequest):
            def login_post(rt, name, password):
                try:
                    password = encryption(name, password)
                except:
                    password = ''
                # 防止sql注入
                if re.match('^\w+$', name) is not None \
                        and sqltool.ifGet(user_table, where=f"{name_lie}='{name}' and {pwd_lie}='{password}'"):
                    request.session['tid'] = name
                    request.session['name'] = sqltool.select('name', user_table, where=f"{name_lie}='{name}'")[0]['name']
                    href = rt.session.get('href', '/')
                    result = HttpResponse(f'window.location.href="{href}?tid={name}";')
                else:
                    result = HttpResponse('alert("账号或密码错误!");')
                return result

            get = runGetFunc(request, lambda request: render(request, '登录注册/登录.html'))
            post = runPostFunc(request, login_post, 'name', 'password')
            func(request, sqltool)
            if get is not None:
                return get
            elif post is not None:
                return post
            else:
                return redirect('/login/')

        return refunc

    return temp


if __name__ == '__main__':
    print(decrypt('all', '4ovdxuT0K6M='))
