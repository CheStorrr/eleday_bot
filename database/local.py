import sqlite3 as sq 

conn = sq.connect('database.db')
cur = conn.cursor()

cur.execute("ALTER TABLE restricted ADD COLUMN restrict_until TIMESTAMP")