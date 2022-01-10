# -*- coding: UTF-8 -*-
"""
@Project ：NewsReport 
@File    ：ScheduleTask.py
@IDE     ：PyCharm 
@Author  ：胖妞
@Date    ：2022/1/10 2:14
"""

# 定时爬取
import os
import sched
import time

schedule = sched.scheduler(time.time, time.sleep)


def perform_command(cmd, inc):
    # 在inc秒后再次运行自己，即周期运行
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    os.system(cmd)


def timming_exe(cmd, inc=60):
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    schedule.run()  # 持续运行，直到计划时间队列变成空为止


print('每10分钟爬取一次')
# 每10分钟爬取一次
timming_exe('python CrawlerNews.py', 60 * 10)
