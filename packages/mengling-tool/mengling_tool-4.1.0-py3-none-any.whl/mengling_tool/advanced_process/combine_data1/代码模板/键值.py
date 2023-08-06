import config
from mengling_tool.spider_tools.spiders import Httpx
from mengling_tool.advanced_process.key_value import KeyValue


class Test(KeyValue):
    def __init__(self, table, dbname, connect: dict, columnclassdict: dict, spider_mode, spider_config: dict, iftz):
        KeyValue.__init__(self, dbname, table, connect,
                          columnclassdict=columnclassdict,
                          key_ifHave_b=self.ifExies('主键'),
                          key_getValue_dts=self.getValue, iftz=iftz,
                          getspiderfunc=spider_mode, spider_config=spider_config)

    def ifExies(self, key):
        return self.getIfHaveFunc_default(key)

    def getValue(self, data):
        spider = self.getGood('spider')
        datadts = [dict()]
        return datadts


if __name__ == '__main__':
    # 参数
    name, dbname, connect = '表名', '库名', config.WORK_CONNECT
    columnclassdict = {}
    spider_mode, spider_config = Httpx, {'proxies': None}
    threadnum = 10
    keys = []

    # 流程
    t = Test(name, dbname, connect, columnclassdict=columnclassdict,
             spider_mode=spider_mode, spider_config=spider_config, iftz=True)
    t.run(keys, threadnum=threadnum)
