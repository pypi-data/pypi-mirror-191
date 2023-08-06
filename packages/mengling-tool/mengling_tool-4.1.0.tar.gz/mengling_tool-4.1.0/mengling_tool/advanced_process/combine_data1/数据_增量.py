from ...functions.thread_tool import SuperTaskClass
from ...functions.goodlib import ThreadDictGoods
from ...database_tool2.mysql import MysqlExecutor
from ...spider_tools.selenium1 import ChromeDriver
from ...spider_tools.spiders.httpx import Httpx


class Increment(SuperTaskClass):
    def __init__(self, dbname, table, connect: dict, key_ifHave_b, key_getValue_dts,
                 columnclassdict: dict = None, driver_config: dict = None,
                 getspiderfunc=Httpx, spider_config: dict = None, iftz=True):
        self.table = table
        self.columnclassdict = columnclassdict if columnclassdict is not None else {}
        self.dtgoods = ThreadDictGoods({'sqltool': [MysqlExecutor, {'dbname': dbname, 'ifassert': True, **connect}],
                                        'driver': [ChromeDriver,
                                                   driver_config if driver_config is not None else {'headless': True}],
                                        None: [lambda **kwargs: None, {}],
                                        'spider': [getspiderfunc, spider_config if spider_config is not None else {}]},
                                       {'driver': lambda x: x.quit(), None: lambda x: x})
        self.__ifHave__ = key_ifHave_b
        self.__getValue__ = key_getValue_dts
        SuperTaskClass.__init__(self, self.__childFunc__, [], cellnum=1, name=table, iftz=iftz)

    # 获取线程资源
    def getGood(self, key):
        return self.dtgoods.getThreadKeyGood(key)

    # 快捷获取判断方法
    def getIfHaveFunc_default(self, keyname):
        def temp(key):
            sqltool = self.dtgoods.getThreadKeyGood('sqltool')
            return sqltool.ifGet(self.table, where=f"`{keyname}`='{key}'")

        return temp

    def __childFunc__(self, key):
        key = key[0]
        dts = self.__getValue__(key)
        sqltool = self.dtgoods.getThreadKeyGood('sqltool')
        try:
            sqltool.insert_create_dt(self.table, *dts, columnclassdict=self.columnclassdict)
            sqltool.commit()
        except:
            sqltool.rollback()
            assert False, f'{key} 数据插入错误! 已回滚'

    def run(self, keys, threadnum=10, maxloopnum: int = -1):
        sqltool = self.dtgoods.getThreadKeyGood('sqltool')
        print('[总量]', len(keys))
        while maxloopnum < 0 or maxloopnum > 0:
            # 表格不存在时不用判断
            if sqltool.ifExist(self.table):
                datast = set([key for key in keys if not self.__ifHave__(key)])
            else:
                datast = set(keys)
            if len(datast) > 0:
                self.datas = datast
                self.threadnum = threadnum
                SuperTaskClass.run(self)
                self.dtgoods.delAllGood()
            else:
                self.dtgoods.delAllGood()
                break
            maxloopnum -= 1
