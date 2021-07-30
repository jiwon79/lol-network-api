import psycopg2 as pg2
import urllib.parse as urlparse
import os

class DBEngine:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connected = False
        self.connect()
    
    def __del__(self):
        self.close()

    def connect(self):
        # if self.connected:
        #     return False
        url = urlparse.urlparse(os.environ['LOL_NETWORK_DATABASE_URL'])
        dbname, user, password, host, port = url.path[1:], url.username, url.password, url.hostname, url.port
 
        self.conn = pg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.connected = True
        return self.conn
    
    def close(self):
        if (not self.connected):
            return False
        self.conn.close()
        self.connected = False
        return True

    # execute sql command
    def execute(self, query, data = None):
        # if (not self.connected):
        #     return False
        self.connect()
        try:
          with self.conn:
            with self.cur:
              self.cur.execute(query, data)
              if (query[:6] == "SELECT" or query[:6] == "select"):
                  rows = self.cur.fetchall()
                  return rows
              return True
        except Exception as e:
            return e
        

# test code
if __name__ == "__main__":    
    db = DBEngine()
    # sql = "INSERT INTO cars (name, price) values (%s, %s);"
    # db.execute(sql, ['name', 1000])
    # sql = "INSERT INTO cars (id, name, price) values (%s, %s, %s);"
    # db.execute(sql, [10, 'name', 1000])
    sql = "SELECT 'id' FROM ip_log ORDER by 'id' DESC LIMIT 1"
    result = db.execute(sql)

    sql = "INSERT INTO ip_logs (ip, request, regdate) values (%s, %s, %s);"
    result = db.execute(sql, ['127.0.0.1', '루모그래프', '20210730225710'])
    # sql = "SELECT * FROM cars"
    # result = db.execute(sql, [])
    print(result) 
    