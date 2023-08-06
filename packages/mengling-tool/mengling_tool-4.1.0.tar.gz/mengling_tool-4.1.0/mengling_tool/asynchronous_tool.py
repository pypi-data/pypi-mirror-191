# -*- coding: UTF-8 -*-
import inspect
import ctypes
import threading
import multiprocessing
import types
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import asyncio
import time
import traceback
from multiprocessing import Manager
import importlib
import func_timeout

'''需要在if __name__=='__main__':的环境下运行'''


# 获取cpu数量
def getCPUNumber():
    return multiprocessing.cpu_count()


# # 获取进程同步对象
# def getManager():
#     # 需要在if __name__=="__main__"下执行
#     return multiprocessing.Manager()


# 不好用，进程出错不会通知
# 进程池
def processPool(maxnum, func, argslist, onevalue=False):
    pool = ProcessPoolExecutor(max_workers=maxnum)
    ps = []
    for args in argslist:
        if onevalue:
            ps.append(pool.submit(func, args))  # 放入单值
        else:
            ps.append(pool.submit(func, *args))  # 执行多值
    # pools.map(func, *argslist)  # 维持执行的进程总数为num，当一个进程执行完毕后会开始执行排在后面的进程
    return pool, ps


# 不好用，线程出错不会通知
# 线程池
def threadPool(maxnum, func, argslist, onevalue=False):
    pool = ThreadPoolExecutor(max_workers=maxnum)
    ps = []
    for args in argslist:
        if onevalue:
            ps.append(pool.submit(func, args))  # 放入单值
        else:
            ps.append(pool.submit(func, *args))  # 执行多值
    # pools.map(func, *argslist)  # 维持执行的进程总数为num，当一个进程执行完毕后会开始执行排在后面的进程
    return pool, ps


# 获取进程同步管理对象
def getProcessManager():
    return Manager()


# 多进程
# 参数不能是自定义类型的实例对象，或者这种实例对象的方法
def process_run(func, argslist: list, ifwait=True):
    ns = []
    for args in argslist:
        n = multiprocessing.Process(target=func, args=tuple(args))
        ns.append(n)
    [n.start() for n in ns]
    if ifwait: [n.join() for n in ns]


# 多线程
def threads_run(func, argslist: list, ifone=False, ifwait=True):
    ns = []
    for args in argslist:
        if ifone: args = (args,)
        n = threading.Thread(target=func, args=tuple(args))
        n.setDaemon(True)  # 设置为守护线程
        ns.append(n)
    [n.start() for n in ns]
    if ifwait: [n.join() for n in ns]


def thread_auto_run(arg_func, args, threadnum: int, ifwait=True, if_return_key_values=False, iftz=True,
                    max_error_num: int = 10) -> list or None:
    in_lock, out_lock = threading.Lock(), threading.Lock()
    args = list(args)
    length = len(args)
    results = list()
    error_num = 0

    def temp():
        nonlocal error_num
        # 接收返回值
        while True:
            with in_lock:
                if len(args) > 0:
                    arg = args.pop(0)
                else:
                    break
            try:
                result = arg_func(arg)
                with out_lock:
                    if if_return_key_values:
                        results.append([arg, result])
                    else:
                        results.append(result)
                    if iftz: print(f'\r{len(results)}/{length}', end='')
            except:
                traceback.print_exc()
                with in_lock:
                    error_num += 1
                    args.append(arg)
                    if iftz: print(f'\r{length - len(args)}/{length}', end='')
                    if error_num > max_error_num:
                        break

    ts = [threading.Thread(target=temp) for i in range(threadnum)]
    [t.start() for t in ts]
    if ifwait:
        [t.join() for t in ts]
        # 返回值判断错误情况
        if len(results) < length:
            raise ValueError(f'{len(results)}/{length} 返回值小于输入值,因任务错误情况提前退出!')
        else:
            return results
    else:
        # 不等待不判断错误情况
        return None


# 协程运行
def tasksRun(*tasks):
    # 返回为list,序列对应协程序列
    if len(tasks) == 1:
        return asyncio.get_event_loop().run_until_complete(asyncio.gather(tasks[0]))
    else:
        return asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))


##仅用于旧版代码,不建议使用
def retryFunc(func):
    def temp(*values, **kwargs):
        index = kwargs.get('index', '')
        ci = kwargs.get('ci', 3)
        sleeptime = kwargs.get('sleeptime', 5)
        sleepfunc = kwargs.get('sleepfunc', time.sleep)
        iftz = kwargs.get('iftz', True)
        iftz = True
        for i in range(1, ci + 1):
            try:
                return func(*values, **kwargs)
            except:
                if iftz:
                    traceback.print_exc()
                    print(index, '失败，正在重试...第', i, '次，休息', sleeptime, '秒')
                if sleeptime > 0: sleepfunc(sleeptime)
        print('错误参数组：', values)
        assert False, '重试全部失败，抛出错误'

    return temp


# 需设置参数
def retryFunc_args(name='', ci=3, sleeptime=5, sleepfunc=time.sleep, iftz=True):
    def retryFunc(func):
        def temp(*values, **kwargs):
            e = None
            for i in range(1, ci + 1):
                try:
                    return func(*values, **kwargs)
                except:
                    e = traceback.format_exc()
                    if iftz:
                        print(e)
                        print(name, '失败，正在重试...第', i, '次，休息', sleeptime, '秒')
                    if sleeptime > 0: sleepfunc(sleeptime)
            print('错误参数组：', values)
            raise ValueError(f'{e}\n重试全部失败，抛出错误')

        return temp

    return retryFunc


# 多任务分配
def getTasks(num, taskdatas):
    tasklen = len(taskdatas)
    if tasklen == 0: return []
    num = min(num, tasklen)
    cellnum = tasklen // num if tasklen % num == 0 else tasklen // num + 1
    tasks = list()
    for i in range(0, tasklen, cellnum):
        tasks.append(taskdatas[i:i + cellnum])
    return tasks


# 重新加载当前导入的所有模块
def reloadAllModel():
    print(dir())
    for model in dir():
        if '__' not in model:
            print(model)
            print(types.ModuleType(model))
            importlib.reload(model)


# 超时机制装饰器
def timeoutRaise_func(timeout, ifraise=True, error_txt='执行超时!'):
    def temp0(func):
        def temp1(*args, **kwargs):
            @func_timeout.func_set_timeout(timeout)
            def temp2():
                return func(*args, **kwargs)

            try:
                return temp2()
            except func_timeout.exceptions.FunctionTimedOut as e:
                print(func, args, kwargs, error_txt)
                if ifraise:
                    raise e
            except Exception as e:
                raise e

        return temp1

    return temp0


# 自定义线程类模型
class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__alive = False

    def start(self):
        threading.Thread.start(self)
        self.__alive = True

    def stop(self):
        self.__alive = False
        stopThread(self)

    def is_alive(self):
        return threading.Thread.is_alive(self) and self.__alive


# 关闭线程
def stopThread(thread):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(thread.ident)
    if not inspect.isclass(SystemExit):
        exctype = type(SystemExit)
    else:
        exctype = SystemExit
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


_SELECT = dict()


# 多项选择方法
def select_parent(name, key, *args, **kwargs):
    return _SELECT[name][key](*args, **kwargs)


# 多项选择装饰器用于注册
def selectFunc_child(name, key=None):
    assert not (_SELECT.get(name) and _SELECT[name].get(key)), f'{name} {key} 已存在!'

    def temp(func):
        _SELECT[name] = _SELECT.get(name, dict())
        _SELECT[name][key] = func
        return lambda *args, **kwargs: func(*args, **kwargs)

    return temp
