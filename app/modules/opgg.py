from fastapi import HTTPException
from bs4 import BeautifulSoup
import json
from aiohttp import ClientSession
from app.core.constant import *
from urllib import parse   
    
async def getUserData(session: ClientSession, nickname: str):
    url = f'https://www.op.gg/summoner/userName={nickname}'

    try:
        async with session.get(url, headers=API_HEADER) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            data = json.loads(
                str(soup.select_one("script#__NEXT_DATA__").contents[0])
            )['props']['pageProps']['data']
            tier_data = data['league_stats'][0]['tier_info']
            
            return {
                'id': data["summoner_id"],
                'name': data['name'],
                'profile_image': data['profile_image_url'],
                'level': data['level'],
                'tier_class': tier_data["tier"],
                'division': tier_data["division"],
                'league_points': tier_data["lp"],
            };
    except Exception:
        raise HTTPException(status_code=404, detail="OPGG crawling failed")
        # raise exceptions.APIFetchError
    
async def getUserFirstHistory(session: ClientSession, user_name: str, id: str):
    url = f'https://lol-api-summoner.op.gg/api/kr/summoners/{id}/games'
    
    try:
        async with session.get(url, headers=API_HEADER) as response:
            data = json.loads(await response.text())['data']
            teamList = []
            for i in range(len(data)):
                team =getTeamUsers(user_name, data[i]['participants'])
                teamList.append(team)
            endTime = data[-1]['created_at']
            return {
                'team_list': teamList,
                'end_time': endTime 
            }
    except Exception:
        raise

async def getUserHistory(session: ClientSession, user_name: str, user_id: str, endTime: str):
    queryList = [('hl', 'ko_KR'), ('game_type', 'TOTAL'), ('ended_at', endTime)]
    query = parse.urlencode(queryList)
    url = f'https://www.op.gg/api/games/kr/summoners/{user_id}?{query}'
    
    try:
        async with session.get(url, headers=API_HEADER) as response:
            data = json.loads(await response.text())
            teamList = []
            for i in range(len(data['data'])):
                team = getTeamUsers(user_name, data['data'][i]['participants'])
                teamList.append(team)
                
            return {
                'team_list': teamList,
                'end_time': data['meta']['last_game_created_at']
            }
    except Exception:
        raise

def getTeamUsers(user_name, user_list):
    blueTeam, redTeam = [], []
    for i in range(10):
        if (user_list[i]['team_key'] == "BLUE"):
            blueTeam.append(user_list[i]['summoner']['name'])
        else:
            redTeam.append(user_list[i]['summoner']['name'])
    return blueTeam if user_name in blueTeam else redTeam

def getResponse(user_data, team_data):
    username = user_data['name']
    profileImg = user_data['profile_image']
    friends = {}
    friendResult = []
    
    for i in range(len(team_data)):
        for member in team_data[i]:
            if (member != username):
                if member in friends:
                    friends[member] += 1
                else:
                    friends[member] = 0 

    for key in friends.keys():
        if friends[key] > 1:
            friendResult.append({key: friends[key]})
    friendResult = sorted(friendResult, key=lambda info: list(info.values())[0], reverse=True)
    
    return {
        "userName": username,
        "profileImage": profileImg,
        "friend": friendResult,
    }