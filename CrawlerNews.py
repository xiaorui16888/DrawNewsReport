# -*- coding: UTF-8 -*-
"""
@Project ：NewsReport 
@File    ：CrawlerNews.py
@IDE     ：PyCharm 
@Author  ：胖妞
@Date    ：2022/1/9 22:26
"""
import DrawReport
import Config
import time


# 爬取并生成海报-可开定时
def updateNews():
    for i, nodes in enumerate(Config.news_nodes):
        for j, node in enumerate(nodes['list']):
            print(i, j)
            time.sleep(2)
            DrawReport.drawCategoryReport(i, j)


if __name__ == '__main__':
    updateNews()
