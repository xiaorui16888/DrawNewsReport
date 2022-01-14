# -*- coding: UTF-8 -*-
"""
@Project ：NewsReport 
@File    ：DrawReport.py
@IDE     ：PyCharm 
@Author  ：胖妞
@Date    ：2022/1/9 22:00
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Config

import requests
import re
import os
import ImageMerge
import QrCodeUtil

nodes = Config.news_nodes


# 生成海报
def drawCategoryReport(category_node=0, platform_node=1):
    category_platform = nodes[category_node]['list'][platform_node]  # 读取节点内容
    url = "https://tophub.today/n/" + category_platform['url']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/55.0.2883.87 Safari/537.36'}
    aaa = requests.get(url, headers=headers).text  # 模拟请求头，访问网页
    title_pattern = re.compile(r'itemid="[0-9]*">(.*?)</a>')  # 正则提取网页中的“今日热议”
    titles = title_pattern.findall(aaa)[0:15]  # 匹配“今日热议”正则十次
    print(titles)
    if len(titles) == 0:  # 如果没有爬取到新闻
        return
    platform_name = category_platform['name']

    # 转换列表准备绘制
    def old_to_new_list(old_list, line_width):
        news_list = []
        for single_text in old_list:
            if title_font.getsize(single_text.strip())[0] < line_width or title_font.getsize(
                    single_text.strip()) == line_width:
                news_list.append(single_text)
            else:
                new_str = ''
                index = 0
                for item in single_text:
                    new_str += item
                    if title_font.getsize(new_str.strip())[0] > line_width:
                        news_list.append(new_str[:-1])
                        new_str = ''
                        if title_font.getsize(single_text[index:])[0] < line_width:
                            news_list.append(single_text[index:])
                        else:
                            break

                    index += 1
        return news_list

    # 绘制列表
    def draw_list(x, y, the_list, line_high):
        for index, info in enumerate(the_list):
            top_height = index * line_high
            draw.text((x, y + top_height + 80), u'%s' % info, title_color, title_font)

    # 获取绘制列表的高度
    def get_draw_list_height(the_list, line_high):
        top_height = 0
        for index, info in enumerate(the_list):
            top_height = index * line_high
        return top_height

    # 转换新闻--列表给信息加上编号，输出列表
    def format_list(inf_origin):
        inf_after = []
        for index, single_info in enumerate(inf_origin):
            inf_after.append(u'%s、%s' % ((index + 1), single_info))
        return inf_after

    font_header_type = './fonts/SourceHanSerifSC-Bold.otf'  # 字体路径
    font_title_type = './fonts/SourceHanSerifSC-Light.otf'  # 字体路径
    header_font = ImageFont.truetype(font_header_type, 35)  # 设置字体
    title_font = ImageFont.truetype(font_title_type, 30)  # 设置字体

    title_color = "#000"  # 新闻标题颜色
    list_x = 60  # 列表起始X坐标
    list_y = 400  # 列表起始Y坐标
    text_line_width = 670  # 列表中，行长度
    text_line_high = 70  # 列表中，行高度

    top = './source/top.png'  # 图片模板-背景图
    bottom = './source/bottom.png'  # 图片模板-背景图
    item = './source/item.png'

    old_news_list = format_list(titles)  # 新闻列表进行转换--加序号
    new_news_list = old_to_new_list(old_news_list, text_line_width)  # 新闻列表进行转换--换行

    images = [top]
    for i in range(143, get_draw_list_height(new_news_list, text_line_high), 143):
        images.append(item)
    images.append(bottom)
    # print(images)
    ImageMerge.image_merge(images=images, output_dir='output',
                           output_name='%s_%s.jpg' % (category_node, platform_node))  # 合并图片，生成背景图
    # print(get_draw_list_height(new_news_list, text_line_high))  # 绘制需要绘制新闻列表的高度

    # 开始画图
    bg_img = '%s/%s_%s.jpg' % ('output', category_node, platform_node)  # 图片模板-背景图
    image = Image.open(bg_img)  # 打开图片
    draw = ImageDraw.Draw(image)  # 创建绘制对象
    width, height = image.size  # 计算背景图的宽和高

    text_header = platform_name  # 新闻类名称
    text_width = title_font.getsize(text_header)  # 分别代表这行字占据的宽和高
    header_x = int((width - text_width[0]) / 2.2)  # 新闻类名称x坐标
    header_y = 365  # 新闻类名称y坐标
    header_color = "#fff"  # 新闻类标题的字体颜色
    draw.text((header_x, header_y), u'%s' % text_header, header_color, header_font)  # 绘制新闻类的标题

    draw_list(list_x, list_y, new_news_list, text_line_high)  # 开始绘制新闻列表

    qr_code = '%s_%s.png' % (bg_img, category_platform['url'])
    QrCodeUtil.makeQrCode('https://tophub.today/n/' + category_platform['url'], qr_code)
    new_img2 = Image.open('./' + qr_code)  # 打开图片
    image.paste(new_img2, (100, height - 325))

    # image.show()  # 展示图片
    img_path = os.path.join('.', bg_img)  # 要保存图片的路径
    image.save(img_path)  # 保存图片
