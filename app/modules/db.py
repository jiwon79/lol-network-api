import psycopg2 as pg2
import urllib.parse as urlparse
import os
from opgg import *

DATABASE_URL = os.environ['LOL_NETWORK_DATABASE_URL']
url = urlparse.urlparse(DATABASE_URL)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

def uploadLog(user_log):
    try:
        with pg2.connect(dbname=dbname, user=user, password=password, host=host, port=port) as conn:
            with conn.cursor() as cur:
                # for log in user_log:
                #     id, time, player, result, team = log['id'], log['time'], log['player'], log['result'], log['team']
                #     sql = f"INSERT INTO log_test VALUES({id}, {time}, '{player}', '{result}', '{team[0]}', '{team[1]}', '{team[2]}', '{team[3]}')"
                #     print(sql)
                #     cur.execute(sql)
                sql = 'ALTER TABLE public.log_test ALTER COLUMN "time" TYPE int USING "time"::int;'
                cur.execute(sql)

                sql = 'ALTER TABLE public.log_test ALTER COLUMN id TYPE int USING id::int;'
                cur.execute(sql)

                cur.execute("SELECT * FROM log_test")
                rows = cur.fetchall()

    except Exception as e:
        print('Error : ', e)
    else:
        print(rows)
    finally:
        if conn:
            conn.close()

if __name__=="__main__":
    user_log = getUserAllGameData("마리마리착마리")
    uploadLog(user_log)