import config
import mengling_tool.spider_tools.spiders as zz
from mengling_tool.advanced_process.组合_数据_单组 import Combination_One
from mengling_tool.spider_tools.selenium工具 import ChromeDriver
import mengling_tool.spider_tools.爬虫工具 as pc
import mengling_tool.spider_tools.解析工具 as jx


class Test(Combination_One):
    def __init__(self, name, dbindex: int, spider_mode, spider_config, iftz):
        Combination_One.__init__(self, name, self.getBase, self.getDts, dbindex=dbindex, iftz=iftz,
                                 getspiderfunc=spider_mode, spider_config=spider_config)

    def getBase(self, key) -> list:
        spider = self.getGood('spider')
        datas = ['']
        pass
        return datas

    # 执行数据获取的单位方法，一个组合一次
    def getDts(self, data) -> list:
        spider = self.getGood('spider')
        datadts = [dict()]
        pass
        return datadts


if __name__ == '__main__':
    # 参数
    dbname, table, dbindex = '库名', '表名', 0
    connect = config.WORK_CONNECT
    spider_mode, spider_config = zz.Httpx, {'proxies': None}
    base_threadnum, threadnum = 3, 5
    keys = []
    columnclassdict = {}

    # 流程
    x = Test(table, dbindex, spider_mode=spider_mode, spider_config=spider_config, iftz=True)
    x.initBase(keys, threadnum=base_threadnum)
    x.run(threadnum=threadnum)
    x.inMysql(dbname, table, ifchecknum=True, ifmyisam=True, connect=connect, columnclassdict=columnclassdict)
