import sqlite3
import pandas as pd
import os  # Pour vérifier si le fichier existe
import json

# Connexion à la base de données
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Sélectionner tous les cyclistes de la table "cyclist"
cur.execute("SELECT id FROM cyclists")
cyclists = cur.fetchall()

for i in range(1, 7):
    with open(f'fast-api/archive/sbj_{i}.json') as f:
        data = json.load(f)

        cyclist_id = cyclists[i][0]
        power = data['power.max']
        vo2max = data['vo2.max']
        cadence=data['cadence.max']
        hr = data['hr.max']
        rf = data['rf.max']


        # Insérer les données dans la table "test_data"
        cur.execute("""
        INSERT INTO tests_data (cyclist_id, vo2max, power, cadence, hr, rf)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (cyclist_id, vo2max, power, cadence, hr, rf))


# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()
