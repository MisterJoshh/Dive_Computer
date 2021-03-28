import sqlite3


class Database:
    def __init__(self,db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS dive (line INTEGER PRIMARY KEY,id integer, depth integer,time integer, temp intager)")
        self.con.commit()

    def insert(self,list):
        if len(list)>5:
            self.cur.executemany('INSERT INTO dive VALUES (Null,?,?,?,?)',list)
            self.con.commit()

    def diveNum(self):
        self.cur.execute('SELECT MAX(id) FROM dive')
        maxid = self.cur.fetchone()[0]
        return maxid+1

    def popLog(self):
        self.cur.execute()