from bs4 import BeautifulSoup
import aiohttp
import time
import json
from aiohttp import ClientSession
from app.core.constant import *
from urllib import parse

GAME_LIMIT = 4  # 100 games
FRIEND_LIMIT = 8

async def getUserData(session: ClientSession, nickname: str):
    url = f'https://www.op.gg/summoner/userName={nickname}'

    try:
        async with session.get(url, headers=API_HEADER) as response:
            soup = BeautifulSoup(
                await response.text(), 'html.parser')
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
        raise
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
    print(url)
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
    

def getAGameData(log, user_name):
    game_data = {"id": 0, "time": 0, "result": "", "team": []}

    gameItem = log.select_one(".GameItem")
    game_data["id"] = gameItem["data-game-id"]
    game_data["time"] = gameItem["data-game-time"]
    game_data["result"] = gameItem["data-game-result"]

    for team in log.select(".Team"):
        if team.select(".Requester") != []:
            for summoner in team.select(".Summoner"):
                if "(Bot)" in summoner.text:
                    break
                name = summoner.select_one(".SummonerName > a").get_text()
                if user_name.replace(" ", "") != name.replace(" ", ""):
                    game_data["team"].append(name)
    return game_data

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