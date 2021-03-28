import sqlite3


class Database:
    def __init__(self,db='db'):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS dive (id INTEGER PRIMARY KEY, depth integer,time integer, temp intager)")
        self.con.commit()

    def insert(self,list):
        self.cur.executemany('INSERT INTO dive (NULL,?,?,?)',list)
        self.con.commit()

    def diveNum(self):
        self.cur.execute('SELECT * FROM dive WHERE id = (SELECT MAX(id) FROM dive)')
        maxid = self.cur.fetchall()
        if len(maxid)==0:
            return 0
        else:
            return int(maxid[0]+1)

            
