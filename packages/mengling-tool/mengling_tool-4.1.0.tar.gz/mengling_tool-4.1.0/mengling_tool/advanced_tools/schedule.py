from ..database_tool2.mysql import MysqlExecutor
from ..notice_tool import emailSend
from ..time_tool3 import TimeTool, getNowTime
import time
from threading import Lock, Thread
import math
import traceback
import sys
import importlib


class Tasker:
    def __init__(self, table, dbname, connect: dict, thread_maxnum=3, sleeptime0: int = 86400):
        # 调度表名
        self.table = table
        # 链接配置
        self.connect = {'dbname': dbname, **connect}
        # 最大线程数
        self.thread_maxnum = thread_maxnum
        # 半天
        self.sleeptime0 = sleeptime0
        self.sleeptime = sleeptime0
        self.logtxts = list()
        self.lock = Lock()

    def log_add(self, txt, window=False):
        self.lock.acquire()
        self.logtxts.append(txt)
        self.lock.release()

    def log_send(self, title):
        txt = '\n'.join(self.logtxts)
        print(txt)
        if '运行失败' in txt: emailSend(title, txt)
        self.logtxts.clear()

    def run_ch(self, taskname, model, func, arg, nowtime, nextime):
        start = time.time()
        print('\n', f'{taskname} 任务开始')
        try:
            arg = arg if arg != '-' else ""
            # 重新加载模块,注意命令严格遵守换行格式
            # 注意：更改了导入模块依赖的模块后，重新加载的函数不会对这些模块生效，需要重启任务调度
            if model != '-':
                ml = f'import {model} as model\nimportlib.reload(model)\nmodel.{func}({arg})'
            else:
                ml = f'{func}({arg})'
            exec(ml)
            end = time.time()
            self.log_add('work_task：%s 运行成功！，运行时间: %s 秒' % (taskname, math.ceil(end - start)))
        except:
            self.log_add('work_task：%s 运行失败！' % taskname)
            temp = traceback.format_exc()
            self.log_add(temp)
        # 更新时间
        try:
            sqltool = MysqlExecutor(**self.connect)
            sqltool.update_dt(self.table, {'上次运行时间': nowtime.to_txt(), '下次运行时间': nextime.to_txt()}, where=f"`任务名`='{taskname}'")
            sqltool.commit()
        except:
            sqltool.rollback()
            self.log_add('表操作失败！')
            temp = traceback.format_exc()
            self.log_add(temp)
        finally:
            sqltool.close()

    def run(self):
        # 重置工具包模块
        [importlib.reload(importlib.import_module(key)) for key in list(sys.modules.keys()) if 'mengling_tool' in key]
        nowtime = getNowTime(ifreturn_str=False)
        self.log_add('任务组开始执行...' + nowtime.to_txt())
        # log_save(nowtime.strftime("%Y_%m_%d"))
        self.sleeptime = self.sleeptime0
        try:
            sqltool = MysqlExecutor(**self.connect)
            taskdts = sqltool.select('*', self.table)
            args = []
            for task in taskdts:
                # 启用选项控制
                if task['启用'] == b'\x00': continue
                # 格式不正确一律视为None值
                try:
                    task['下次运行时间'] = TimeTool(task['下次运行时间'])
                    task['上次运行时间'] = TimeTool(task['上次运行时间'])
                except:
                    task['下次运行时间'], task['上次运行时间'] = None, None
                if task['下次运行时间'] is None or task['下次运行时间'] < nowtime:
                    if nowtime.to_txt(gs='%H:%M:%S') < task['时刻']:
                        # 早跑
                        temptime = nowtime
                    else:
                        # 晚跑
                        temptime = nowtime.next(task['周期'], ifreturn_str=False)
                    # 月度定时处理
                    if 31 >= task['月度'] > 0:
                        b = False
                        for i in range(345):
                            temptime.next(1, if_replace=True)
                            if temptime.date.day == task['月度']:
                                b = True
                                break
                        if not b: raise ValueError(f'月度设置有问题 {task["月度"]}')
                    # 计算下次运行时间
                    nextime = TimeTool(temptime.to_txt(gs="%Y/%m/%d ") + task['时刻'])
                    # 根据周末设置进行下次运行时间的调整
                    if task['周末'] != b'\x00' and nextime.isoweekday() in [6, 7]:
                        nextime.next(8 - nextime.isoweekday(), if_replace=True)

                    arg = [task['任务名'], task['模块'], task['方法'], task['参数'], nowtime, nextime]
                    self.log_add('work_task:%s 运行开始...' % task['任务名'])
                    # log_save(nowtime.strftime("%Y_%m_%d"))
                    args.append(arg)
            # 多线程运行
            ts = [Thread(target=self.run_ch, args=args[i]) for i in range(min(self.thread_maxnum, len(args)))]
            [t.start() for t in ts]
            [t.join() for t in ts]
            # 计算下次运行时间
            sqltool.refresh()
            dates = sqltool.select('下次运行时间', self.table, where="`启用`=1", ifget_one_lie=True)
            sqltool.close()
            mintime = TimeTool(min(dates))
            nowtime = getNowTime(ifreturn_str=False)
            if nowtime > mintime:
                self.sleeptime = 3
            else:
                self.sleeptime = math.ceil(min(self.sleeptime, mintime - nowtime + 3))
        except:
            self.log_add('任务组执行出错，请及时查看！')
            temp = traceback.format_exc()
            self.log_add(temp)
        self.log_add('开始等待下一次任务...%d秒\n' % self.sleeptime)
        self.log_send('%s任务组执行日志' % self.table)
        for i in range(self.sleeptime):
            print('\r剩余时间：%s 秒     ' % (self.sleeptime - i), end='')
            time.sleep(1)
