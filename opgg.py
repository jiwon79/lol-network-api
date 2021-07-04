import requests
from bs4 import BeautifulSoup
import json

def get_user_info(user_name: str):
    url = f'https://www.op.gg/summoner/userName={user_name}'

    game_data = {
        'gameId': 0,
        'team': [],
        'gameResult': ''
    }
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        if soup.select_one('.SummonerNotFoundLayout') is not None:
            return {}
        summonerId = soup.select_one('.GameListContainer')['data-summoner-id']
        logs = soup.select("div.GameItemWrap")
        id, time = [], []

        for log in logs:
            id.append(log.select_one('.GameItem')['data-game-id'])
            time.append(log.select_one('.GameItem')['data-game-time'])
        print(len(id), len(time))
        print('log 갯수 : ', len(logs))

        while(True):
            print("After GET requests")
            more_url = f'https://op.gg/summoner/matches/ajax/averageAndList/startInfo={time[-1]}&summonerId={summonerId}'
            
            more_response = requests.get(more_url)
            if more_response.status_code != 200:
                break
            more_html = more_response.json()['html']
            more_soup = BeautifulSoup(more_html, 'html.parser')
            logs = more_soup.select("div.GameItemWrap")
            
            for log in logs:
                id.append(log.select_one('.GameItem')['data-game-id'])
                time.append(log.select_one('.GameItem')['data-game-time'])
            print(len(id), len(time))
            
    else:
        raise Exception('fetch fail')

# test code
if __name__ == '__main__':
    from pprint import pprint
    # moreInfo();

    # get_user_info('꿀벌지민')   # Ranked user
    get_user_info('베이스또털어')
    