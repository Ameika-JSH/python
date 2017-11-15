import sqlite3 as sql

db = sql.connect('sqlite.db')
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS SLTABLE (PATH TEXT,CREATED DATETIEM)')
cur.execute('INSERT INTO SLTABLE VALUES("TestPath",datetime("now","localtime"))')
db.commit()
