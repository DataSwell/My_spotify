import os
import psycopg2

# password for the database from an environment variable
db_pw = os.environ.get('DB_PASS')
conn_str = "host=localhost user=postgres dbname=My_Spotify password={}".format(db_pw)

class MyDatabase():
    def __init__(self):
        self.conn = psycopg2.connect(conn_str)
        self.cur = self.conn.cursor()

        self.conn.set_session(autocommit=True)

    def query_func(self, query, params=None):
        try:
            self.cur.execute(query, params)
        except psycopg2.Error as e:
            print(e)

    def fetchall(self,query):
        try:
            self.cur.execute(query)
        except psycopg2.Error as e:
            print(e)
        return self.cur.fetchall()

    def fetchone(self, query):
        try:
            self.cur.execute(query)
        except psycopg2.Error as e:
            print(e)
        return self.cur.fetchone()

    def close(self):
        self.cur.close()
        self.conn.close()
