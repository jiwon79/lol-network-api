import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
LIMIT = -1

def getAGameData(log, user_name):
    game_data = {
        'id': 0,
        'time': 0,
        'player': user_name,
        'result': '',
        'team': []
    }

    game_data['id'] = log.select_one('.GameItem')['data-game-id']
    game_data['time'] = log.select_one('.GameItem')['data-game-time']

    for team in log.select('.Team'):
        if (team.select('.Requester') != []):
            for summoner in team.select('.Summoner'):
                name = summoner.select_one('.SummonerName > a').get_text()
                if (user_name.replace(" ","") != name.replace(" ","")):
                    game_data['team'].append(name)
    
    result =  log.select_one('.GameResult').get_text()
    if ('victory' in result):
        game_data['result'] = 'Victory'
    else:
        game_data['result'] = 'Defeat'
        
    return game_data

def getUserAllGameData(user_name: str):
    count = 0
    game_data_list = []

    url = f'https://www.op.gg/summoner/userName={user_name}'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # if summoner doesn't exist, return {}
        if soup.select_one('.SummonerNotFoundLayout') is not None:
            return {}

        summonerId = soup.select_one('.GameListContainer')['data-summoner-id']
        logs = soup.select("div.GameItemWrap")

        for log in logs:
            game_data = getAGameData(log, user_name)
            game_data_list.append(game_data)

        # while no information, requests matches data
        while(True):
            if (count == LIMIT):
                break
            count += 1

            # print("GET requests")
            start_time = game_data_list[-1]['time']
            more_url = f"https://op.gg/summoner/matches/ajax/averageAndList/startInfo={start_time}&summonerId={summonerId}"
            
            more_response = requests.get(more_url)
            if more_response.status_code != 200:
                break
            more_html = more_response.json()['html']
            more_soup = BeautifulSoup(more_html, 'html.parser')
            logs = more_soup.select("div.GameItemWrap")
                
            for log in logs:
                game_data = getAGameData(log, user_name)
                game_data_list.append(game_data)
        # pprint(game_data_list)
        return game_data_list
            
    else:
        raise Exception('fetch fail')

# test code
if __name__ == '__main__':
    # getUserAllGameData('꿀벌지민')   # Ranked user
    getUserAllGameData('마리마리착마리')
    