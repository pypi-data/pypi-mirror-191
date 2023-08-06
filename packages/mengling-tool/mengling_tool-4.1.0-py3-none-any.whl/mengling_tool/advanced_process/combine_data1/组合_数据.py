import json,time
from math import inf
from pandas import DataFrame
from ...asynchronous_tool import retryFunc_args
from ...database_tool2.redis import RedisExecutor
from ...functions.thread_tool import SuperTaskClass
from ...functions.goodlib import ThreadDictGoods
from ...functions.progress_tool import jdprint
from ...database_tool2.mysql import MysqlExecutor
from ...time_tool1 import runTimeFunc, getNowDatetime
from ...spider_tools.selenium2 import ChromeDriver
from ...spider_tools.spiders.httpx import Httpx


class Combination(SuperTaskClass):
    def __init__(self, name, data_getBase_jstxt, datas_getDatadtsFunc_basedt,
                 dbindex, redis_connect, ci=3, cellnum=1,
                 getdriverfunc=ChromeDriver, driver_config: dict = None,
                 getspiderfunc=Httpx, spider_config: dict = None, ifdayupdate=False,
                 iftz=False):
        self.__getbase__ = data_getBase_jstxt
        self.__getdatadtsfunc__ = datas_getDatadtsFunc_basedt
        # 表名同样作为其他的名称
        self.name = name
        self.name_config = '%s_config' % name
        self.name_wait = '%s_wait' % name
        self.name_ready = '%s_ready' % name
        self.iftz = iftz
        self.__ci = ci
        # 用于判断是否为更新类型的任务
        self.ifdayupdate = ifdayupdate
        self.__nowday__ = getNowDatetime(returnstr=True)
        self.dtgoods = ThreadDictGoods({'r': [RedisExecutor, {'dbindex': dbindex, **redis_connect}],
                                        'driver': [getdriverfunc,
                                                   driver_config if driver_config is not None else {'headless': True}],
                                        None: [lambda **kwargs: None, {}],
                                        'spider': [getspiderfunc,
                                                   spider_config if spider_config is not None else {}], },
                                       {'driver': lambda x: x.quit(), None: lambda x: x})
        SuperTaskClass.__init__(self, self.__childFunc__, [], cellnum=cellnum, name=self.name, iftz=iftz)
        # 用于控制单位执行速度
        self.__sleeptime__, self.__first__ = 0, True

    # 可用于新增新的字典
    def inputRedis(self, name_hz, key, value):
        r = self.getGood('r')
        r.hset(f'{self.name}_{name_hz}', key, value)

    # 获取线程资源
    def getGood(self, key):
        return self.dtgoods.getThreadKeyGood(key)

    def __cellBase(self, bs):
        r = self.getGood('r')

        @retryFunc_args(name='获取组合', ci=self.__ci, iftz=self.iftz)
        def getBase(b0):
            return self.__getbase__(b0)

        for b0 in bs:
            b0_txt = str(b0)
            # 检查是否已存在
            if r.ifExist(self.name_config, b0_txt, _class='hash'):
                if self.iftz: jdprint('%s 已存在,跳过' % b0_txt)
            else:
                # 获取全部组合
                try:
                    bases = getBase(b0)
                except:
                    print('[组合错误]', b0)
                    continue
                if len(bases) > 0:
                    # r.addData(self.name_ready, *bases, _class='set')
                    r.addData(self.name_wait, *bases, _class='set')
                r.addData(self.name_config, {b0_txt: len(bases)}, _class='hash')

    # 初始化基础组合
    def initBase(self, bs, threadnum=1):
        self.childFunc = self.__cellBase
        self.datas = bs
        self.threadnum = threadnum
        SuperTaskClass.run(self)
        # 更换方法
        self.childFunc = self.__childFunc__
        self.datas = []
        self.dtgoods.delAllGood()

    # 获取未完成组合
    def getIncompleteBases(self):
        r = self.getGood('r')
        return r.getData(self.name_wait, _class='set') - set(r.hkeys(self.name))

    # 一对一映射组合初始化方法
    def initBase_one(self, bs, n=20_0000):
        # 统一插入
        bs = list(bs)
        print('统一更新组合...')
        r = self.getGood('r')
        for i in range(0, len(bs), n):
            bases = list(map(str, bs[i:i + n]))
            print(i, '-', i + n)
            dt = dict()
            for base in bases:
                dt[base] = 1
            r.hmset(self.name_config, dt)
            r.sadd(self.name_wait, *bases)
        # 更换方法
        self.childFunc = self.__childFunc__
        self.datas = []
        self.dtgoods.delAllGood()

    def __save__(self, data, datadts):
        r = self.getGood('r')
        r.addData(self.name, {data: json.dumps(datadts)}, _class='hash')

    def __childFunc__(self, datas):
        if self.__sleeptime__ > 0 and not self.__first__:
            print(f'等待休息{self.__sleeptime__}s...')
            time.sleep(self.__sleeptime__)
        if self.__first__: self.__first__ = False
        base_dts_dt = self.__getdatadtsfunc__(datas)
        # 数据格式清洗
        for base in base_dts_dt.keys():
            for dt in base_dts_dt[base]:
                for key in dt.keys():
                    key = str(key).strip()
                    # 全部定义为字符串类型
                    dt[key] = str(dt[key]).strip()
            # 记录
            self.__save__(base, base_dts_dt[base])

    def run(self, threadnum=10, getnum=10_0000, maxloop=inf, sleeptime=0):
        self.threadnum = threadnum
        self.__sleeptime__ = sleeptime
        while maxloop > 0:
            maxloop -= 1
            print(f'整理未完成组合...单组数量：{getnum}')
            r = self.getGood('r')
            self.datas = r.spop(self.name_ready, getnum)
            if len(self.datas) > 0:
                print(f'当前完成进度：{r.getLen(self.name, _class="hash")}/{r.getLen(self.name_wait, _class="set")}')
                SuperTaskClass.run(self)
            else:
                # 检测数量并进行预备池清理
                if r.getLen(self.name, _class='hash') < r.getLen(self.name_wait, _class='set'):
                    s = list(self.getIncompleteBases())
                    for i in range(0, len(s), 20_0000):
                        cs = s[i:i + 20_0000]
                        r.addData(self.name_ready, *cs, _class='set')
                else:
                    break
            self.dtgoods.delAllGood()
        self.dtgoods.delAllGood()
        if maxloop == 0: print('已循环至最大限制,可能存在未完成组合')

    # 完成指定的数据集即可
    def run_datas(self, datas, threadnum=10, maxloop=inf):
        r = self.getGood('r')
        self.threadnum = threadnum
        datas = set(datas)
        tempdatas = datas - set(r.hkeys(self.name))
        while len(tempdatas) > 0 and maxloop > 0:
            self.datas = tempdatas
            print(f'当前完成进度：{len(datas) - len(tempdatas)}/{len(datas)}')
            SuperTaskClass.run(self)
            self.dtgoods.delAllGood()
            # 检测数量并进行预备池清理
            tempdatas = datas - set(r.hkeys(self.name))
            maxloop -= 1
        return tempdatas

    def getAllValues(self):
        r = self.getGood('r')
        dts = list()
        [dts.extend(json.loads(txt)) for txt in r.hvals(self.name)]
        return dts

    @runTimeFunc
    def inMysql(self, dbname, table, connect, lies=None, columnclassdict: dict = None, key=None, threadnum=10,
                ifmyisam=False, ifdeltable=True, n=50_0000,
                ifdelredis=False, iforce_delredis=False, ifchecknum=True):
        sqltool = MysqlExecutor(dbname, ifassert=True, **connect)
        r = self.getGood('r')
        if self.ifdayupdate:
            print(self.__nowday__)
            if sqltool.ifGet(table, where=f"`更新日期`='{self.__nowday__}'"):
                print('此任务的更新日期也存在,不做插入操作!')
                sqltool.close()
                self.dtgoods.delThreadKeyGood()
                return
        jdprint('读取及处理redis数据...')
        if ifchecknum:
            assert r.getLen(self.name, _class='hash') == r.getLen(self.name_wait), \
                f'数量不一致,不执行插入数据库任务! {r.getLen(self.name, _class="hash")}/{r.getLen(self.name_wait)}'
        allkeys = r.hkeys(self.name)
        all_value_len = 0
        # 判断创建表创建表
        if ifdeltable and not self.ifdayupdate: sqltool.deleteTable(table)
        if not sqltool.ifExist(table):
            if lies is None:
                jsons = r.hmget(self.name, allkeys[:n])
                values = list()
                for j in jsons:
                    dts = json.loads(j)
                    values.extend(dts)
                lies = list(DataFrame(data=values).columns)
            assert len(lies) > 0
            if self.ifdayupdate: lies.append('更新日期')
            sqltool.createTable(table, lies, columnclassdict=columnclassdict if columnclassdict is not None else {},
                                key=key, ifmyisam=ifmyisam)

        for i in range(0, len(allkeys), n):
            jsons = r.hmget(self.name, allkeys[i:i + n])
            values = list()
            for j in jsons:
                dts = json.loads(j)
                values.extend(dts)
            jdprint('插入mysql...%s' % n)
            all_value_len += len(values)
            # 增加更新日期
            if self.ifdayupdate:
                for dt in values: dt['更新日期'] = self.__nowday__
            sqltool.thread_insert_commit(table, values, lies=lies, threadnum=threadnum, ifcreate=False)

        if ifdelredis or iforce_delredis:
            # 强制删除
            if not iforce_delredis:
                where = f"`更新日期`='{self.__nowday__}'" if self.ifdayupdate else 'true'
                count = sqltool.select('count(1)', table, where=where, data_class='ls')[0][0]
                assert count == all_value_len, 'redis数据量与表中数据量不一致,redis数据未删除!'
            r.delete(self.name, self.name_wait, self.name_config)
            print(f'已{"强制" if iforce_delredis else "检查"}清理redis数据...')
        sqltool.close()
        self.dtgoods.delThreadKeyGood()


if __name__ == '__main__':
    pass
