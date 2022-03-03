from bs4 import BeautifulSoup
from pprint import pprint
import aiohttp
import time
import json
from aiohttp import ClientSession
from app.core.constant import *

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
            # print(data[0]['participants'])
            teamList = []
            for i in range(len(data)):
                team =getTeamUsers(user_name, data[i]['participants'])
                teamList.append(team)
            endedAt = data[-1]['created_at']
            # print(getTeamUsers(user_name, data[0]['participants']))
            return {
                'team_list': teamList,
                'ended_at': endedAt 
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

    
async def getUserAllGameData(user_name: str):
    print(user_name)
    count = 0
    result = {"player": user_name, "profileImage": "", "summonerId": 0, "gameData": []}
    game_data_list = []
    url = f"https://www.op.gg/summoner/userName={user_name}"
    start_time = time.time()
    async with aiohttp.ClientSession(headers=API_HEADER) as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("fetch fail")
            response_text = await response.text()
    soup = BeautifulSoup(response_text, "html.parser")
    
    # if summoner doesn't exist, return {}
    if soup.select_one(".SummonerNotFoundLayout") is not None:
        return {}
    result["profileImage"] = "https:" + soup.select_one(".ProfileImage")["src"]
    summonerId = int(soup.select_one(".GameListContainer")["data-summoner-id"])
    result["summonerId"] = summonerId

    logs = soup.select("div.GameItemWrap")
    for log in logs:
        game_data = getAGameData(log, user_name)
        game_data_list.append(game_data)
    print(len(game_data))

    # while no information, requests matches data
    while True:
        if count == GAME_LIMIT:
            break
        count += 1

        # print("GET requests")
        start_time = game_data_list[-1]["time"]
        more_url = f"https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo={start_time}&summonerId={summonerId}"
        print(more_url)
        async with aiohttp.ClientSession(headers = headers) as session:
            async with session.get(more_url) as more_response:
                if more_response.status != 200:
                    break
                more_json = await more_response.read();
        more_html = json.loads(more_json)['html']
        more_soup = BeautifulSoup(more_html, "html.parser")
        logs = more_soup.select("div.GameItemWrap")

        for log in logs:
            game_data = getAGameData(log, user_name)
            game_data_list.append(game_data)
        print(len(game_data_list))
    result["gameData"] = game_data_list
    return result


def getUserFrield(user_log):
    team, friend = {}, []
    for log in user_log["gameData"]:
        for member in log["team"]:
            if member in team:
                team[member] += 1
            else:
                team[member] = 0

    for key in team.keys():
        if team[key] > 1:
            friend.append({key: team[key]})
    friend = sorted(friend, key=lambda info: list(info.values())[0], reverse=True)

    result = {
        "userName": user_log["player"],
        "profileImage": user_log["profileImage"],
        "friend": friend,
    }
    return result


# test code
# if __name__ == "__main__":
    # user_log = getUserAllGameData("마리마리착마리")
    # friend = getUserFrield(user_log)
    # pprint(friend)