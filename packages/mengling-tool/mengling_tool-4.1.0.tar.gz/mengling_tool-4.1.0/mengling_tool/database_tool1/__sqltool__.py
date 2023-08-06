import base64
import threading
import traceback
import pandas as pd
from pyDes import PAD_PKCS5, CBC, des

__Des_Key0 = '%s&@W2*<FRW2'
__Des_IV = b'\x52\x63\x78\x61\xBC\x48\x6A\x07'


def encryption(user, passwd):
    k = des((__Des_Key0 % user)[:8], CBC, __Des_IV, padmode=PAD_PKCS5)
    return base64.b64encode(k.encrypt(passwd)).decode('utf-8')


def decrypt(user, passwd_enc):
    k = des((__Des_Key0 % user)[:8], CBC, __Des_IV, padmode=PAD_PKCS5)
    return k.decrypt(base64.b64decode(passwd_enc)).decode('utf-8')


# 表格去重
def table_drop_duplicates(dts: list, *lies) -> pd.DataFrame:
    df = pd.DataFrame(data=dts)
    df.drop_duplicates(subset=lies, keep='first', inplace=True)
    return df


# 模板工具
class TemplateSQLTool:
    def __init__(self, db, cursor, connect, ifassert, iftz, default_lie_class='varchar(255)'):
        self.connect = connect
        self.ifassert = ifassert
        self.iftz = iftz
        # 打开数据库连接
        self.db = db
        self.cursor = cursor
        self.default_lie_class = default_lie_class

    # 使用sql操作
    def run(self, sql, datas=None, ifdatas=False, ifgetdatadts=False, **kwargs):
        try:
            ##不再用datas进行插入
            # 执行sql语句
            if datas is None:
                self.cursor.execute(sql)
            else:
                # datas中也为列表
                self.cursor.executemany(sql, datas if type(datas[0]) in (tuple, list) else [datas])
            # 列名
            if self.cursor.description is None:
                lies = list()
            else:
                lies = [lc[0] for lc in self.cursor.description]
            if not ifdatas:
                datas_result = None
            else:
                temp_results = self.cursor.fetchall()
                datas_result = list()
                for row in temp_results:
                    templs, tempdt = list(), dict()
                    for i in range(len(lies)):
                        lie, data = lies[i], row[i]
                        if type(data) == str: data = data.strip()
                        if ifgetdatadts:
                            tempdt[lie] = data
                        else:
                            templs.append(data)
                    if ifgetdatadts:
                        datas_result.append(tempdt)
                    else:
                        datas_result.append(templs)
            return [lies, datas_result]
        except:
            if self.ifassert:
                traceback.print_exc()
                assert False
            else:
                if self.iftz:
                    print(sql)
                    print('datas:', str(datas)[:100], '...')
                print(traceback.format_exc())
                if ifdatas:
                    return None, None
                else:
                    return None

    def close(self):
        try:
            self.db.close()
        except:
            pass

    '''事务操作'''

    # 提交事务
    def commit(self):
        self.db.commit()

    # 事务回滚
    def rollback(self):
        self.db.rollback()

    def getTablestr(self, table, **kwargs):
        return table

    def getLiestrs(self, lies, **kwargs):
        if lies == '*' or lies == 'count(1)':
            return [lies]
        else:
            if type(lies) == str: lies = [lies]
            lies = [('`%s`' % lie.replace('%', '%%')) for lie in lies]
            return lies

    def getValuestrs(self, values, **kwargs):
        valuestrs = ["'%s'" % (str(value).replace("'", "\\'").strip()) for value in values]
        return valuestrs

    # 获取整合后的总列
    def getAllLies(self, dts):
        liedt = dict()
        for dt in dts:
            for key in dt.keys():
                if liedt.get(key) is None:
                    liedt[key] = 0
        return list(liedt.keys())

    '''增删查改'''

    # 查询,会有事物隔离的情况出现,可以重新生成对象进行查询
    def select(self, lies, table, where='True', other='', ifgetdatadts=False, ifgetonelie=False, **kwargs):
        sql = '''select {lies}
                from {table}
                where {where}
                {other}
        '''.format(lies=','.join(self.getLiestrs(lies, **kwargs)), table=self.getTablestr(table, **kwargs), where=where,
                   other=other)
        lies, datas = self.run(sql, ifdatas=True, ifgetdatadts=ifgetdatadts and not ifgetonelie, **kwargs)
        if ifgetonelie:
            return [d[0] for d in datas]
        else:
            return lies, datas

    # 判断是否可以查询到
    def ifGet(self, table, where='True', **kwargs):
        try:
            num = self.select('count(1)', table, where=where, **kwargs)[1][0][0]
        except:
            traceback.print_exc()
            num = 0
        if num > 0:
            return True
        else:
            return False

    # 插入
    def insert(self, table: str, lies: list, *all_values, **kwargs):
        length = len(lies)
        assert length > 0, "列数量不能为0！"
        allvaluestrs = list()
        # 单列插入
        if kwargs.get('ifonelie', False):
            for value in all_values:
                allvaluestrs.append([str(value).strip()])
        else:
            for values in all_values:
                assert len(values) == length, f'列数与值数不一致!{len(values)},{length}'
                allvaluestrs.append(list(map(lambda x: str(x).strip(), values)))
        # 插入语句
        sql = '''INSERT INTO {table}({liestr})
                VALUES ({cstr})
        '''.format(table=self.getTablestr(table, **kwargs), liestr=','.join(self.getLiestrs(lies, **kwargs)),
                   cstr=','.join(['%s' for i in range(length)]))
        self.run(sql, datas=allvaluestrs, **kwargs)

    # 批量插入字典,需要保证所有字典键值一致
    # 如果没有指定列,则会取第一个字典的列作为标准列,没有的部分其他字典会有默认值,但是多出的部分不会被记录
    def insert_create_dt(self, table: str, *dts, lies=None, ifcreate=True, columnclassdict: dict = None, key=None,
                         **kwargs):
        if len(dts) == 0: return
        lies = self.getAllLies(dts) if lies is None else lies
        values = list()
        for dt in dts:
            temps = list()
            for lie in lies:
                value = dt.get(lie, '')
                value = '' if value is None else value
                temps.append(value)
            values.append(temps)
        if ifcreate: self.createTable(table, lies, columnclassdict=columnclassdict, key=key, **kwargs)
        self.insert(table, lies, *values)

    def thread_insert_commit(self, table, dts, lies=None, columnclassdict: dict = None, key=None,
                             threadnum=10, ifcreate=True, **kwargs):
        if columnclassdict is None:
            columnclassdict = {}
        lies = self.getAllLies(dts) if lies is None else lies
        if ifcreate: self.createTable(table, lies, columnclassdict=columnclassdict, key=key, **kwargs)
        length = len(dts) // threadnum
        threads = list()
        print('[线程插入数] %s' % threadnum)

        def temp(table, dts):
            sqltool = type(self)(self.dbname, ifassert=True, **self.connect)
            try:
                sqltool.insert_create_dt(table, *dts, lies=lies, ifcreate=False, **kwargs)
                sqltool.commit()
            except:
                print('出现错误,该批数据执行单条插入')
                for dt in dts:
                    try:
                        sqltool.insert_create_dt(table, dt, lies=lies, ifcreate=False, **kwargs)
                        sqltool.commit()
                    except:
                        print('[出错]', dt)
                        sqltool.rollback()
            sqltool.close()

        for i in range(threadnum):
            if i == threadnum - 1:
                dts_ch = dts[i * length:]
            else:
                dts_ch = dts[i * length:i * length + length]
            arg = [table, dts_ch]
            t = threading.Thread(target=temp, args=tuple(arg))
            t.start()
            threads.append(t)
        [t.join() for t in threads]

    def insert_create_df(self, table: str, df: pd.DataFrame,
                         columnclassdict: dict = None, key=None, ifcreate=True, **kwargs):
        lies = [lie.strip() for lie in df.columns.values]
        if ifcreate: self.createTable(table, lies, columnclassdict=columnclassdict, key=key, **kwargs)
        rows = list()
        for index, row in df.iterrows():
            rows.append(row.values.tolist())
        if len(rows) > 0: self.insert(table, lies, *rows, **kwargs)

    # 删除
    def delete(self, table, where: str, **kwargs):
        # 表名
        sql = '''DELETE FROM {table}
            WHERE {where}
        '''.format(table=self.getTablestr(table, **kwargs), where=where)
        self.run(sql, **kwargs)

    # 修改
    def update(self, table, lies: list, values: list, where: str, **kwargs):
        assert len(lies) > 0 and len(lies) == len(values), "数量有误！"
        setv = ','.join([(lie + '=%s') for lie in self.getLiestrs(lies, **kwargs)])
        sql = '''UPDATE {table}
                SET {setv}
                WHERE {where}
        '''.format(table=self.getTablestr(table, **kwargs), setv=setv, where=where)
        # print(sql)
        self.run(sql, datas=values, **kwargs)

    '''表操作'''

    # 创建表
    def createTable(self, table, lies: list, columnclassdict: dict = None, key=None, **kwargs):
        # CREATE TABLE table_name (column_name column_type);  Create Table If Not Exists
        if columnclassdict is None:
            columnclassdict = {}
        assert len(lies) > 0, "数量有误！"
        # 列类型进行默认赋值
        for lie in lies:
            columnclassdict[lie] = columnclassdict.get(lie, self.default_lie_class)
        # Create Table If Not Exists
        if key is not None:
            if type(key) == str: key = [key]
            if key != '*': key = " ,PRIMARY KEY(%s)" % ','.join(self.getLiestrs(key, **kwargs))
        else:
            key = ''
        # 不再使用null，默认为空字符
        liestr = ",".join([("%s %s " % (self.getLiestrs([lie], **kwargs)[0], columnclassdict[lie]) +
                            ("NOT NULL DEFAULT ''" if columnclassdict[lie] == 'varchar(255)' else ''))
                           for lie in lies])
        sql = '''
            Create Table If Not Exists {table}
            ({lies} {key})
        '''.format(table=self.getTablestr(table, **kwargs), lies=liestr, key=key)
        self.run(sql, **kwargs)

    # 删除表
    def deleteTable(self, table, **kwargs):
        # DROP TABLE table_name
        sql = '''DROP TABLE IF EXISTS {table} 
        '''.format(table=self.getTablestr(table, **kwargs))
        self.run(sql, **kwargs)

    # 删除列
    def deleteColumn(self, table, liename, **kwargs):
        # ALTER TABLE tablename  DROP i;
        sql = '''ALTER TABLE {table} 
                DROP {liename}
        '''.format(table=self.getTablestr(table, **kwargs), liename=liename)
        self.run(sql, **kwargs)

    # 修改列属性
    def setColumn(self, table, liename, newname, dataclass="VARCHAR(255)", **kwargs):
        lies = self.getLiestrs([liename, newname])
        sql = '''ALTER TABLE {table} 
                CHANGE {liename} {newname} {dataclass}
        '''.format(table=self.getTablestr(table, **kwargs), liename=lies[0], newname=lies[1], dataclass=dataclass)
        self.run(sql, **kwargs)

    # 新增列
    def addColumn(self, table, liename, dataclass="VARCHAR(255)", other="", **kwargs):
        # ALTER TABLE `tcl科技 (深证:000100)` add `昨日收盘` VARCHAR(255) AFTER `今日收盘`
        sql = '''ALTER TABLE {table}
                ADD {liename} {dataclass} 
                {other}
        '''.format(table=self.getTablestr(table, **kwargs), liename=self.getLiestrs(liename)[0], dataclass=dataclass,
                   other=other)
        self.run(sql, **kwargs)

    # 将表中所有字段的null替换为空字符
    def replaceNULL(self, table):
        lies, datas = self.select('*', table)
        row_news = []
        for row in datas:
            row_news.append([d if d is not None else '' for d in row])
        # 清空表数据
        self.delete(table, 'True')
        [self.insert(table, lies, row) for row in row_news]
        self.commit()


if __name__ == '__main__':
    print(encryption('txadmin', ''))
