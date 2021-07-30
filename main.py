from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import *

from app.modules.opgg import *
from app.database.Model import *
app = FastAPI()

origins = [
    'http://lol-network.netlify.app/',
    'https://lol-network.netlify.app/',
    'http://lol-network.netlify.app',
    'https://lol-network.netlify.app',
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3002',
    'http://localhost:5500',
    'http://localhost:5501',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3001',
    'http://127.0.0.1:3002',
    'http://127.0.0.1:5500',
    'http://127.0.0.1:5501',
    'http://127.0.0.1:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

dummy_data = {
    'node': [
        {'id': '마리마리착마리', 'value': 1},
        {'id': '루모그래프', 'value': 1},
        {'id': '꿀벌지민', 'value': 1},
        {'id': '리듬타지마', 'value': 1}
    ],
    'edge': [
        {'from': '마리마리착마리', 'to': '루모그래프', 'value': 10},
        {'from': '마리마리착마리', 'to': '꿀벌지민', 'value': 5},
        {'from': '루모그래프', 'to': '꿀벌지민', 'value': 15},
        {'from': '루모그래프', 'to': '리듬타지마', 'value': 3},
        {'from': '꿀벌지민', 'to': '리듬타지마', 'value': 1}
    ]
}

@app.get("/")
def read_root():
    return dummy_data

@app.get("/userlog/{user_name}")
def get_user_log(user_name: str):
    user_log = getUserAllGameData(user_name)
    return user_log

@app.get("/friend/{user_name}")
def get_user_friend(request: Request, user_name: str):
  # insert ip logs
  model = Model()
  client_host = request.client.host
  now = datetime.now().strftime('%Y%m%d%H%M%S')
  model.insertIpLog([client_host, user_name, now])

  user_log = getUserAllGameData(user_name)
  if (user_log == {}):
    return {"result": "no-summoner"}
  
  friend = getUserFrield(user_log)
  return friend

@app.get("/ip")
def get_ip(request: Request):
  client_host = request.client.host
  return {"client_host": client_host}

@app.get("/insertIPLog/{name}")
def connect_db(request: Request, name: str):
  model = Model()
  client_host = request.client.host
  now = datetime.now()
  nowDatetime = now.strftime('%Y%m%d%H%M%S')
  
  result = model.insertIpLog([client_host, name, nowDatetime])
  result = {
    "client_host": client_host,
    "name": name,
    "date": nowDatetime
  }
  return result

# if __name__ == "__main__":
#     user_name = "마리마리착마리"
#     user_log = getUserAllGameData(user_name)
#     friend = getUserFrield(user_log)
#     print(friend)    
