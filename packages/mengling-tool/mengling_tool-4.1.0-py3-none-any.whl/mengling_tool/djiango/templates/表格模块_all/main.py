import os, json
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, Http404
from django.shortcuts import render
from math import ceil


class Tabler:
    def __init__(self, request: WSGIRequest, sqlt, identifier='`%s`',
                 cookie_name0='table', table_width='', table_height='',
                 helpdt: dict = None):
        self.req = request
        self.sqlt = sqlt
        self.identifier = identifier
        self.cookie_name0 = cookie_name0
        self.table_width = table_width
        self.table_height = table_height
        # self.title = title
        self.helpdt = helpdt if helpdt else dict()

    def getWhere(self):
        ikey_values = []
        for i in ['1', '2', '3']:
            key, value = self.req.GET.get(f'fkey{i}', ''), self.req.GET.get(f'fvalue{i}', '')
            if len(key) > 0 and len(value) > 0:
                ikey_values.append((i, key, value.strip()))
        wheres = ['1=1']
        for i, k, v in ikey_values:
            if self.req.GET.get('mh' + i, '0') == '1':
                s1 = "{k} like '%{v}%'"
            else:
                s1 = "{k} = '{v}'"
            wheres.append(s1.format(k=self.identifier % k, v=v))
        return ' and '.join(wheres)

    # 新增、修改或删除操作
    def update(self, table, and_where='1=1'):
        datadt = json.loads(self.req.body)
        # where
        vr = lambda v: v.replace("'", "\\'")
        where = ' and '.join(
            [f"{self.identifier % k}='{vr(v)}'" for k, v in datadt.get('old', dict()).items()] + [and_where])
        if datadt.get('new') is None:
            # 删除操作
            print('删除表数据', table)
            self.sqlt.delete(table, where=where)
        elif datadt.get('old') is None:
            # 新增操作
            print('新增表数据', table)
            self.sqlt.insert_create_dt(table, datadt['new'], ifcreate=False)
        else:
            # 修改操作
            print('修改表数据', table)
            self.sqlt.update_dt(table, datadt['new'], where=where)
        self.sqlt.commit()

    def getOther(self, cellnum: int = None):
        page = max(int(self.req.GET.get('page', 1)), 0)
        order_name, order = self.req.GET.get('okey', ''), self.req.GET.get('ovalue', 'down')
        if len(order_name) > 0:
            other = f'order by {self.identifier % order_name} {"desc" if order == "down" else "asc"} '
        else:
            other = ''
        if cellnum:
            other += f'limit {cellnum} offset {page * cellnum - cellnum}'
        return other

    def getDownload(self, file_path):
        with open(file_path, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
            except Exception:
                raise Http404

    # 用于合并主数据生成表格
    def _parentRows(self, parent_lies, dts):
        # 同类列数据合并
        key_rows = dict()
        for dt in dts:
            key = tuple(dt.pop(lie, '') for lie in parent_lies)
            if key_rows.get(key) is None: key_rows[key] = list()
            key_rows[key].append(dt)
        # 表格字段生成
        rows = list()
        for key, ch_dts in key_rows.items():
            first = True
            for ch_dt in ch_dts:
                if first:
                    row = dict((lie, {'text': k, 'rowspan': len(ch_dts)}) for k, lie in zip(key, parent_lies))
                    first = False
                else:
                    row = dict((lie, dict()) for lie in parent_lies)
                row.update(ch_dt)
                rows.append(row)
        return rows

    def getTable(self, table, cellnum: int,
                 lies='*', rowdts: list = None, parent_lies=None,
                 maxnum: int = 0,
                 if_view_find=False, finds: list = None, find_num=3,
                 if_view_lie=False, def_view_lies: list = None,
                 addurl: str = None, updateurl: str = None, downloadurl: str = None,
                 updatelies: list = None, select_liedt: dict = None,
                 if_return_rep=True, html_template='表格模块_all/body.html',
                 **kwargs
                 ):
        if rowdts is None:
            rowdts = self.sqlt.select(lies, table, where=self.getWhere(), other=self.getOther(cellnum))
        if type(lies) == str:
            lies = list(rowdts[0].keys()) if rowdts else []
        if parent_lies:
            rowdts = self._parentRows(parent_lies, rowdts)
            # 开启合并表格功能后不再允许编辑操作
            updateurl, addurl = None, None
        finds = finds if finds else lies
        addurl = addurl if addurl else ''
        page = max(int(self.req.GET.get('page', 1)), 0)
        find_num = min(find_num, 3) if find_num > 0 else 1

        mapdt = {'rowdts': rowdts, 'lies': lies, 'page': page, 'maxpage': ceil(maxnum / cellnum),
                 'if_view_lie': 'true' if if_view_lie else 'false',
                 'if_view_find': 'true' if if_view_find else 'false',
                 'finds': finds, 'find_num': find_num,
                 'def_view_lies': def_view_lies if def_view_lies else [],
                 'cookie_name0': self.cookie_name0,
                 'table_width': self.table_width if self.table_width else '',
                 'table_height': self.table_height if self.table_height else '',
                 'helpdt': self.helpdt,
                 'addurl': addurl,
                 'updateurl': updateurl if updateurl else '',
                 'updatelies': updatelies if updatelies else [],
                 'downloadurl': downloadurl if downloadurl else '',
                 'select_liedt': select_liedt if select_liedt else dict(),
                 **kwargs}
        if if_return_rep:
            return render(self.req, html_template, mapdt)
        else:
            return mapdt
