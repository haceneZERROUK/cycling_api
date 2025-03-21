import sqlite3


conn = sqlite3.connect('database.db')
cur = conn.cursor()

cyclists_data = [
    ('sbj_1', 'm', 22.1, 67.9, 185, 4650, 360, 134, 286, 333),
    ('sbj_2', 'm', 25.6, 79.2, 182.4, 5892, 420, 144, 322, 388),
    ('sbj_3', 'm', 42.8, 81.9, 173.8, 4320, 318, 104, 234, 287),
    ('sbj_4', 'f', 21.6, 66.2, 165.9, 3693, 300, 96, 219, 273),
    ('sbj_5', 'm', 46.6, 81.1, 181, 4120, 300, 96, 216, 270),
    ('sbj_6', 'm', 28.8, 74.4, 171, 4520, 347, 108, 243, 308),
    ('sbj_7', 'm', 22.1, 67.9, 185, 4650, 360, 134, 286, 333,),
]

for c in cyclists_data:
    cur.execute("""
    INSERT INTO cyclists (name, gender, age, weight, height, vo2max, ppo, p1, p2, p3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, c)


    conn.commit()
conn.close()