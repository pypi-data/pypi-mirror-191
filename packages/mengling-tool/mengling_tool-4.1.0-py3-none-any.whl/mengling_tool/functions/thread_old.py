from threading import Lock,get_ident
import time
import traceback
from ..asynchronous_tool import threads_run
# 同层级依赖!
from . import progress_tool as jds


class SuperTaskClass:
    def __init__(self, args_data_childFunc, datas: list, **kwargs):
        """
        :param childFunc: 单位执行方法，参数组：(thread_args,data)
        :param datas: 数据组
        """
        # 线程数
        self.threadnum = kwargs.get('threadnum', 5)
        self.childFunc = args_data_childFunc
        # 参数组
        self.datas = datas
        self.name = kwargs.get('name', '任务组')
        # 错误组
        self.errors = []
        self.getCellArgs = kwargs.get('getCellArgs', lambda: None)
        self.ifChildThreadStrat = kwargs.get('args_ifChildThreadStrat', lambda x: True)
        self.childThreadOver = kwargs.get('args_childThreadOver', lambda x: None)
        self.__lock0 = Lock()  # 互斥锁，获取锁定
        self.__lock1 = Lock()  # 互斥锁，进度显示锁定

    def run(self):
        self.datas = list(self.datas)
        length = len(self.datas)
        if length == 0: return None
        if length < self.threadnum: self.threadnum = length
        jd = jds.Progress(len(self.datas), self.name)

        def temp():
            nonlocal self, jd
            # 单位线程初始化操作
            thread_args = self.getCellArgs()
            if not self.ifChildThreadStrat(thread_args):
                error = '[提前结束]%s' % get_ident()
                print(error)
                self.errors.append(error)
                return None
            while True:
                self.__lock0.acquire()  # 上锁 注意了此时锁的代码越少越好
                if len(self.datas) > 0:
                    data = self.datas.pop(0)
                    self.__lock0.release()  # 解锁
                else:
                    self.__lock0.release()  # 解锁
                    # 没有任务，结束子线程
                    break
                try:
                    self.childFunc(thread_args, data)
                except:
                    print(traceback.format_exc())
                    error = '[严重错误]参数组 ' + str(data) + ' 失败'
                    print(error)
                    self.errors.append(error)
                    # 出错的重新载入
                    # self.datas.append(data)
                # 进度显示
                self.__lock1.acquire()  # 上锁 注意了此时锁的代码越少越好
                jd.add()
                jd.printProgress()
                self.__lock1.release()  # 解锁
            self.childThreadOver(thread_args)

        start = time.time()
        print('任务开始...线程数：%s' % self.threadnum)
        threads_run(temp, [[] for i in range(self.threadnum)], ifwait=True)
        end = time.time()
        print('%s 运行时间: %s 秒' % (self.name, round(end - start, 2)))
