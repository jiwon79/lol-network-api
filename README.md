# LOL-network  
LOL-network 웹사이트 백엔드  
Client : https://lol-network.netlify.com/  
Server : https://lol-network-api.herokuapp.com/  

## Introduction
### Project Schedule
제작기간 : 2021/06 ~ 현재
2021/07 부터 배포 

## Tech Stack
1. Python (FastAPI, Beautiful Soup)
2. heroku

## EndPoints

/data/{username}\
유저의 기본 데이터를 가저옴

/firsthistory/{username}\
유저의 첫 20게임을 가져옴

/history/{username}\
유저의 최근 100게임 정보를 가져옴

/friends/{username}
유저와 같이 플레이한 사람 목록을 가져옴
