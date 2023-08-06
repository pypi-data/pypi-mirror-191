from .组合_数据 import Combination as Combination
import time


class Combination_One(Combination):
    def __init__(self, name, str0_getBase_strs, data_getDatadtsFunc_dts, dbindex,redis_connect,**kwargs):
        Combination.__init__(self, name, str0_getBase_strs, data_getDatadtsFunc_dts,
                             dbindex, redis_connect,
                             cellnum=1, **kwargs)

    def __childFunc__(self, datas):
        if self.__sleeptime__ > 0 and not self.__first__:
            print(f'    等待休息{self.__sleeptime__}s...')
            time.sleep(self.__sleeptime__)
        if self.__first__: self.__first__ = False
        data = datas[0]
        datadts = self.__getdatadtsfunc__(data)
        # 数据格式清洗
        for dt in datadts:
            for key in dt.keys():
                # 全部定义为字符串类型
                dt[key] = str(dt[key]).strip()
        # 记录
        self.__save__(data, datadts)


if __name__ == '__main__':
    pass
