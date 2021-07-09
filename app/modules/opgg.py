import requests
from bs4 import BeautifulSoup
from pprint import pprint
LIMIT = -1

def getAGameData(log, user_name, summonerId):
    game_data = {
        'id': 0,
        'time': 0,
        'player': user_name,
        'result': '',
        'summonerId': summonerId,
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
    game_data_list = []

    url = f'https://www.op.gg/summoner/userName={user_name}'
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # if summoner doesn't exist, return {}
        if soup.select_one('.SummonerNotFoundLayout') is not None:
            return {}

        summonerId = int(soup.select_one('.GameListContainer')['data-summoner-id'])

        logs = soup.select("div.GameItemWrap")
        for log in logs:
            game_data = getAGameData(log, user_name, summonerId)
            game_data_list.append(game_data)

        # while no information, requests matches data
        while(True):
            # if (count == LIMIT):
            #     break
            # count += 1

            # print("GET requests")
            start_time = game_data_list[-1]['time']
            more_url = f"https://op.gg/summoner/matches/ajax/averageAndList/startInfo={start_time}&summonerId={summonerId}"
            headerList = [{"key":"accept","value":"application/json, text/javascript, */*; q=0.01","description":""},{"key":"accept-language","value":"ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6","description":""},{"key":"accept-encoding","value":"gzip, deflate, br","description":""},{"key":"cookie","value":"Hm_lvt_29884b6641f1b5709cc89a8ce5a99366=1625403801; Hm_lpvt_29884b6641f1b5709cc89a8ce5a99366=1625403801; _fbp=fb.1.1625403802945.1755401786; wcs_bt=55c48ac9e22bec:1625403803; _hist=%EB%A7%88%EB%A6%AC%EB%A7%88%EB%A6%AC%20%EC%B0%A9%EB%A7%88%EB%A6%AC; _lr_geo_location=KR; _clck=1xndp49; _pbjs_userid_consent_data=3524755945110770; _ga=GA1.2.152757262.1625403801; _gid=GA1.2.2026993031.1625403804; __gads=ID=34fc8f5ef4b8b397:T=1625403571:S=ALNI_MalWn8YxRXNAbnxIh5U3GmIP8N6KQ; _clsk=373l4q|1625403806612|1|0|eus2/collect; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22a4ff9d43-1b3c-4502-ad0f-d16691065d7c%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-06-04T12%3A59%3A33%22%7D; sharedid=%7B%22id%22%3A%2201F8R9RP59WE40362CB8G2988T%22%2C%22ts%22%3A1625403808114%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-07-04T12%3A59%3A34.279168Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5-ZHMOv6mvzmrKhOFfqARZAyewR_xOnmGuxEy-iakmuQ!ID5*9kWR6ROkc2jGx1hH86XY_68qbOFQQ0LHAsmQGCWk-h8AAHH0IvG9cNi0IgCNFXSO%22%2C%22universal_uid%22%3A%22ID5-ZHMO94Qloh6SiwZ7ZqjFdQecGaLB_Fzesgw9dFiUfA!ID5*z4pUrmJGPEOLUJLn7qSxJODFhfg3A-W9S3AV3OGajZ0AAIEVEAn4eupgsIabiWhz%22%2C%22signature%22%3A%22ID5_AYoCWTJd49kDkgNw8088MscjdxSF25pD7gfciYcPi8smRLOI0uRD9rWc0DMYTLf2TLLXvxoNyGEFygl7HQfmim0%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; pbjs-id5id_last=Sun%2C%2004%20Jul%202021%2013%3A03%3A28%20GMT; _ga_HKZFKE5JEL=GS1.1.1625403800.1.1.1625403879.0; _ga_37HQ1LKWBE=GS1.1.1625403800.1.1.1625403879.0; _dd_s=rum=0&expire=1625404794568","description":""},\
                {"key":"referer","value":"https://www.op.gg/summoner/userName=%EA%BF%80%EB%B2%8C%EC%A7%80%EB%AF%BC","description":""},\
                {"key":"sec-ch-ua","value":"\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"","description":""},{"key":"sec-ch-ua-mobile","value":"?0","description":""},{"key":"sec-fetch-dest","value":"empty","description":""},{"key":"sec-fetch-mode","value":"cors","description":""},{"key":"sec-fetch-site","value":"same-origin","description":""},{"key":"user-agent","value":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36","description":""},{"key":"x-datadog-origin","value":"rum","description":""},{"key":"x-datadog-parent-id","value":"3957892532878851014","description":""},{"key":"x-datadog-sampled","value":"1","description":""},{"key":"x-datadog-sampling-priority","value":"1","description":""},{"key":"x-datadog-trace-id","value":"6311504273084070946","description":""},{"key":"x-requested-with","value":"XMLHttpRequest","description":""}]
            header = {}
            for head in headerList:
                header[head['key']] = head['value']            
            
            more_response = requests.get(more_url, headers=header)
            return {"result": more_response.status_code}
            if more_response.status_code != 200:
                return {"result": more_response.status_code}
                break
            more_html = more_response.json()
            return more_html
            more_html = more_html['html']

            more_soup = BeautifulSoup(more_html, 'html.parser')
            logs = more_soup.select("div.GameItemWrap")
            print(logs)
            for log in logs:
                game_data = getAGameData(log, user_name, summonerId)
                game_data_list.append(game_data)
        # pprint(game_data_list)
        return game_data_list
            
    else:
        raise Exception('fetch fail')

def getUserFrield(user_log):
    team, friend = {}, []
    for log in user_log:
        for member in log['team']:
            if member in team:
                team[member] += 1
            else:
                team[member] = 0
    for key in team.keys():
        if team[key] > 1:
            friend.append({key: team[key]})
    return friend

# test code
if __name__ == '__main__':
    user_log = getUserAllGameData('꿀벌지민')
    pprint(user_log)
    pprint(type(user_log))
    # print(len(user_log))
#     friend = getUserFrield(user_log)
#     print(friend)