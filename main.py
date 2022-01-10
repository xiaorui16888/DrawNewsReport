# -*- coding: UTF-8 -*-
"""
@Project ：NewsReport
@File    ：main.py
@IDE     ：PyCharm
@Author  ：胖妞
@Date    ：2022/1/8 16:00
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()


@app.get('/news/{category}/{platform}')
async def news(category: int, platform: int):
    file_like = open('./output/%s_%s.jpg' % (category, platform), mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=7890, reload=True, debug=True)
