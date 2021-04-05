import sqlite3
import pandas


class Database:
    def __init__(self,db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS dive (id INTEGER PRIMARY KEY,dive_num integer, depth integer,time integer, temp intager)")
        self.con.commit()

    def insert(self,list):
        if len(list)>5:
            self.cur.executemany('INSERT INTO dive VALUES (Null,?,?,?,?)',list)
            self.con.commit()

    def diveNum(self):
        self.cur.execute('SELECT MAX(dive_num) FROM dive')
        maxid = self.cur.fetchone()[0]
        if maxid is None:
            maxid = 0
        return maxid+1

    def popLog(self):
        df_table = pandas.read_sql_query('SELECT * FROM dive',self.con, 'id')
        df_log = df_table.groupby('dive_num').agg({'depth':'max','time':'max','temp':'min'})
        log = []
        for index in range((df_log.shape[0])):
            log.append(f'Dive number:{index+1} Max Depth:{df_log.iloc[index,0]} Length:{df_log.iloc[index,1]} Bottom temp:{df_log.iloc[index,2]} ')
        return log

if __name__=="__main__":
    db = Database('dive_log.db')
    db.popLog()
    #print(db.diveNum())