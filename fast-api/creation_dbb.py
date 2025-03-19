import sqlite3


conn = sqlite3.connect('database.db')


cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS cyclist(
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
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cyclist_id INTEGER,
    username TEXT,
    password TEXT,
    FOREIGN KEY (cyclist_id) REFERENCES cyclist(id)
)
""")


cur.execute("""
CREATE TABLE IF NOT EXISTS test_data(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cyclist_id INTEGER,
    type_test TEXT,
    time INTEGER,
    power INTEGER,
    oxygen REAL,
    cadence INTEGER,
    hr REAL,
    rf REAL,
    FOREIGN KEY (cyclist_id) REFERENCES cyclist(id)
)
""")

conn.commit()
conn.close()