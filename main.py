from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import *
import time
import asyncio
import aiohttp

from app.modules.opgg import *
from app.core.constant import *
from app.schemas.user import *

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

@app.get("/")
async def read_root():
    return {"result": "결과"}

@app.get("/data/{user_name}", response_model=User)
async def get_user_data(user_name: str):
    async with aiohttp.ClientSession() as session:
        user_data = await getUserData(session, user_name)
        return user_data;

@app.get("/firstHistory/{user_name}", response_model=History)
async def get_user_first_history(user_name: str):
    async with aiohttp.ClientSession(headers=API_HEADER) as session:
        user_data = await getUserData(session, user_name)
        user_first_history = await getUserFirstHistory(session, user_data['name'], user_data['id'])
        return user_first_history
    
@app.get("/oldhistory/{user_name}")
async def get_user_history(user_name: str):
    team_data = []
    
    async with aiohttp.ClientSession(headers=API_HEADER) as session:
        user_data = await getUserData(session, user_name)
        user_first_history = await getUserFirstHistory(session, user_data['name'], user_data['id'])
        for i in range(len(user_first_history['team_list'])):
            team_data.append(user_first_history['team_list'][i])

        for i in range(4):
            user_history = await getUserHistory(session, user_data['name'], user_data['id'], user_first_history['end_time'])
            if (len(team_data)%20 != 0):
                break
            for i in range(len(user_history['team_list'])):
                team_data.append(user_history['team_list'][i])
        result = getResponse(user_data, team_data)
        return result

@app.get("/history/{user_name}")
async def get_user_history(user_name: str):
    team_data = []
    
    async with aiohttp.ClientSession(headers=API_HEADER) as session:
        user_data = await getUserData(session, user_name)
        user_first_history = await getUserFirstHistory(session, user_data['name'], user_data['id'])
        for i in range(len(user_first_history['team_list'])):
            team_data.append(user_first_history['team_list'][i])

        for i in range(4):
            user_history = await getUserHistory(session, user_data['name'], user_data['id'], user_first_history['end_time'])
            if (len(team_data)%20 != 0):
                break
            for i in range(len(user_history['team_list'])):
                team_data.append(user_history['team_list'][i])
        result = getFriendsResponse(user_data, team_data)
        return result
