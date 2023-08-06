from math import ceil
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from mengling_tool.数据库工具.mysql工具 import MysqlExecutor

__connect__ = {}
__table__ = ''
__cellnum__ = 10
__html_path__ = ''
__action__ = '/table/'
__title__ = '页面标题'


def getPage(request: WSGIRequest):
    sqltool = MysqlExecutor(**__connect__)

    page = int(request.GET.get('page', 1))
    find_key, find_value = request.GET.get('find_key', None), request.GET.get('find_value', None)
    find_key1, find_value1 = request.GET.get('find_key1', None), request.GET.get('find_value1', None)
    find_key2, find_value2 = request.GET.get('find_key2', None), request.GET.get('find_value2', None)
    order_name, order = request.GET.get('order_name', '录入时间'), request.GET.get('order', 'down')
    ifmh = request.GET.get('ifmh', '0') == '1'

    # 权限控制
    where = ['true']
    pass
    if find_key is not None and find_value is not None:
        for f, v in [(find_key, find_value), (find_key1, find_value1), (find_key2, find_value2)]:
            if f != '无':
                where.append(f"`{f}` like '%{v}%'" if ifmh else f"`{f}` = '{v}'")
    where = ' and '.join(where)

    maxnum = sqltool.getNum(__table__, where)
    dts = sqltool.select('*', __table__, where=where,
                         other=f"order by `{order_name}` {'DESC' if order == 'down' else 'ASC'} limit {(page - 1) * __cellnum__},{__cellnum__}")
    liedts = list()
    lies = list(dts[0].keys()) if len(dts) > 0 else []
    for dt in dts:
        liedt = dict()
        # 权限字段显示
        for lie in lies:
            value = dt.get(lie, '')
            liedt[lie] = f'<td>{value}</td>'
        liedts.append(liedt)

    sqltool.close()
    return render(request, __html_path__,
                  {'action': __action__, 'name': request.session['name'],
                   'liedts': liedts, 'finds': lies,
                   'title': __title__, 'page': page,
                   'maxpage': max(ceil(maxnum / __cellnum__), 1)})
