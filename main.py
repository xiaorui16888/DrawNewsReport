# -*- coding: UTF-8 -*-
"""
@Project ：NewsReport
@File    ：main.py
@IDE     ：PyCharm
@Author  ：胖妞
@Date    ：2022/1/8 16:00
"""
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()


@app.get('/news/poster/{category}/{platform}')
def newsPoster(category: int, platform: int):
    file_like = open('./output/%s_%s.jpg' % (category, platform), mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")


@app.get('/news/text/{category}/{platform}')
def newsText(category: int, platform: int):
    with open("./json/%s_%s.json" % (category, platform), 'r', encoding='utf-8') as load_f:
        return json.load(load_f)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=7890, reload=True, debug=True)
