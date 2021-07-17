from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time

from app.modules.opgg import *
from app.modules.utils import *
import tasks

from rq import Queue
from worker import conn
app = FastAPI()

origins = [
    'http://streamer-network.netlify.app/',
    'https://streamer-network.netlify.app/',
    'http://streamer-network.netlify.app',
    'https://streamer-network.netlify.app',
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

@app.get("/user/{user_name}")
def get_user_friend(user_name: str):
    user_log = getUserAllGameData(user_name)
    friend = getUserFrield(user_log)
    return friend

@app.get("/userlog/{user_name}")
def get_user_log(user_name: str):
    user_log = getUserAllGameData(user_name)
    return user_log

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/rq")
def rqQueue():
    q = Queue(connection=conn)
    result = q.enqueue(count_words_at_url, "http://heroku.com")
    return {"result": result, "Queue": q, "value": result.return_value}

@app.get("/empty")
def clearQueue():
    q = Queue(connection=conn)
    q.empty()
    return {"result" : "success"}

@app.get("/que")
def clearQueue():
    q = Queue(connection=conn)
    return {"result" : "success"}

@app.get("/queue")
def printQueue():
    q = Queue(connection=conn)
    return {"result": q}

def add():
    a, b = 3, 4
    return a+b

@app.get("/rqtest")
def rqtest():
    q = Queue(connection=conn)
    result = q.enqueue(add)
    return {"result": result, "value": result.return_value}

@app.get("/rqtest2")
def rqtest():
    q = Queue(connection=conn)
    result = q.enqueue(add)
    return {"value": result.return_value}

@app.get("/wait")
def wait():
    q = Queue(connection=conn)
    done = False
    r = q.enqueue(add)
    while not done:
        result = r.return_value
        if result is None:
            done = False
        time.sleep(1)
    return {"value": result}

@app.get("/task")
def task():
    result = tasks.addFunc.delay(1,2)
    return {"result", result}
    
# if __name__ == "__main__":
#     user_name = "마리마리착마리"
#     user_log = getUserAllGameData(user_name)
#     friend = getUserFrield(user_log)
#     print(friend)    
