import sqlite3


conn = sqlite3.connect('database.db')


cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS cyclists(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    gender TEXT,
    age REAL,
    weight REAL,
    height REAL,
    vo2max INTEGER,
    ppo INTEGER,
    p1 INTEGER,
    p2 INTEGER,
    p3 INTEGER
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cyclist_id INTEGER,
    username TEXT,
    password TEXT,
    fonction TEXT,
    FOREIGN KEY (cyclist_id) REFERENCES cyclist(id)
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS tests_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cyclist_id INTEGER,
    power INTEGER,
    vo2max REAL,
    cadence REAL,
    hr REAL,
    rf REAL,
    FOREIGN KEY (cyclist_id) REFERENCES cyclist(id)
)
""")

conn.commit()
conn.close()