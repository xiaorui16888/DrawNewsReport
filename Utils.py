# -*- coding: UTF-8 -*-
"""
@Project ：DrawNewsReport 
@File    ：Utils.py
@IDE     ：PyCharm 
@Author  ：胖妞
@Date    ：2022/1/14 19:26
"""
import json


def dict2json(file_name, the_dict):
    # try:
    json_str = json.dumps(the_dict, indent=4, ensure_ascii=False)
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json_str)
    return 1


# except:
#     return 0


if __name__ == '__main__':
    data = {
        'category': '012',
        'platform': '7788',
        'url': '123456',
        'news': ['123', '456', '789']
    }
    dict2json('url.json', data)
