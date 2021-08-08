import requests
from bs4 import BeautifulSoup
from pprint import pprint
GAME_LIMIT = 4 # 100 games
FRIEND_LIMIT = 8

def getAGameData(log, user_name):
    game_data = {
        'id': 0,
        'time': 0,
        'result': '',
        'team': []
    }

    gameItem = log.select_one('.GameItem')
    game_data['id'] = gameItem['data-game-id']
    game_data['time'] = gameItem['data-game-time']
    game_data['result'] = gameItem['data-game-result']

    for team in log.select('.Team'):
        if (team.select('.Requester') != []):
            for summoner in team.select('.Summoner'):
                name = summoner.select_one('.SummonerName > a').get_text()
                if (user_name.replace(" ","") != name.replace(" ","")):
                    game_data['team'].append(name)        
    return game_data


def getUserAllGameData(user_name: str):
    count = 0
    result = {
        'player': user_name,
        'profileImage': '',
        'summonerId': 0,
        'gameData': []
    }
    game_data_list = []

    url = f'https://www.op.gg/summoner/userName={user_name}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # if summoner doesn't exist, return {}
        if soup.select_one('.SummonerNotFoundLayout') is not None:
            return {}

        result['profileImage'] = "https:" + soup.select_one('.ProfileImage')['src']
        summonerId  = int(soup.select_one('.GameListContainer')['data-summoner-id'])
        result['summonerId'] = summonerId

        logs = soup.select("div.GameItemWrap")
        for log in logs:
            game_data = getAGameData(log, user_name)
            game_data_list.append(game_data)

        # while no information, requests matches data
        while(True):
            if (count == GAME_LIMIT):
                break
            count += 1

            # print("GET requests")
            start_time = game_data_list[-1]['time']
            more_url = f"https://www.op.gg/summoner/matches/ajax/averageAndList/startInfo={start_time}&summonerId={summonerId}"                            
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
            more_response = requests.get(more_url, headers=header)
            if more_response.status_code != 200:
                break
            more_html = more_response.json()['html']
            more_soup = BeautifulSoup(more_html, 'html.parser')
            logs = more_soup.select("div.GameItemWrap")

            for log in logs:
                game_data = getAGameData(log, user_name)
                game_data_list.append(game_data)
        result['gameData'] = game_data_list
        # pprint(game_data_list)
        return result
    else:
        raise Exception('fetch fail')

def getUserFrield(user_log):
    team, friend = {}, []
    for log in user_log['gameData']:
        for member in log['team']:
            if member in team:
                team[member] += 1
            else:
                team[member] = 0

    for key in team.keys():
        if team[key] > 1:
            friend.append({key: team[key]})
    friend = sorted(friend, key = lambda info: list(info.values())[0], reverse=True)

    result = {
      "userName": user_log['player'],
      "profileImage": user_log['profileImage'],
      "friend": friend
    }
    return result

# test code
if __name__ == '__main__':
    user_log = getUserAllGameData('마리마리착마리')
    friend = getUserFrield(user_log)
    pprint(friend)