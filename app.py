import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from fund_pegging import pegging
from mt5 import main as mt5_main

app = FastAPI()


# 定义 /event-invoke 的请求体
class Item(BaseModel):
    Type: str
    TriggerName: str
    Time: str
    Message: str


# 腾讯事件函数
@app.post('/event-invoke')
async def invoke(item: Item):
    # 运行监听(腾讯云云函数不会等待异步任务结束，所以这里自行等待)
    await asyncio.create_task(pegging())
    await asyncio.create_task(mt5_main())

    return {"message": "Ok!"}


@app.get("/")
async def root():
    return {"message": "Hello World"}
