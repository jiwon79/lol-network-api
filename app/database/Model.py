import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from conn import DBEngine

class Model():
    def __init__(self):
        self.db = DBEngine()
    
    def getAllGameData(self):
        sql = "SELECT * FROM log_test"
        result = self.db.execute(sql)
        return result
    
    def insertUserLog(self, user_log):
        for log in user_log:
            id, time, player, result, summonerId, team = log['id'], log['time'], log['player'], log['result'], log['summonerId'], log['team']
            sql = "INSERT INTO log_test values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = [id, time, player, result, summonerId, team[0], team[1], team[2], team[3]]
            self.db.execute(sql, data)
        return True

if __name__ == "__main__":
    db = Model()
    result = db.getAllGameData()
    print(result)