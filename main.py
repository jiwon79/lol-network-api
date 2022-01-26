from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import *
import time
import uvicorn

import aiohttp

from app.modules.opgg import *

app = FastAPI()

origins = [
  
    "http://lol-network.netlify.app/",
    "https://lol-network.netlify.app/",
    "http://lol-network.netlify.app",
    "https://lol-network.netlify.app",
    "http://lol-network-dev.netlify.app/",
    "https://lol-network-dev.netlify.app/",
    "http://lol-network-dev.netlify.app",
    "https://lol-network-dev.netlify.app",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:5500",
    "http://localhost:5501",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
async def read_root():
    return {"result": "결과"}


@app.get("/userlog/{user_name}")
async def get_user_log(user_name: str):
    user_log = getUserAllGameData(user_name)
    return user_log


@app.get("/friend/{user_name}")
async def get_user_friend(user_name: str):
    user_log = await getUserAllGameData(user_name)
    if user_log == {}:
        return {"result": "no-summoner"}

    friend = getUserFrield(user_log)
    return friend


@app.get("/ip")
async def get_ip(request: Request):
    client_host = request.client.host
    return {"client_host": client_host}


@app.get("/duration/{duration}")
async def waitDuration(duration: int):
    for i in range(duration):
        print(i + 1)
        time.sleep(1)
    return {"result": "end"}


@app.get("/apitest")
async def test_api():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    }
    url = f"https://www.op.gg/summoner/userName=마리마리착마리"
    # response = requests.get(url, headers=headers)
    # return {'result': 'endd'}

    print("start")
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            print(await response.text())

    return {"result": "end"}
