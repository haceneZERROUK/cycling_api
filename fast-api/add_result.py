import sqlite3
import pandas as pd
import os  # Pour vérifier si le fichier existe

# Connexion à la base de données
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Sélectionner tous les cyclistes de la table "cyclist"
cur.execute("SELECT id FROM cyclist")
cyclists = cur.fetchall()

# Liste des tests
list_test = ['I', 'II', 'incremental', 'Wingate']

for i in range(1, 7):
    for elem in list_test:
        # Formater le nom du fichier CSV
        filename = f'fast-api/archive/sbj_{i}_{elem}.csv'
        
        # Vérifier si le fichier existe avant de le lire
        if os.path.exists(filename):
            try:
                # Lire le fichier CSV
                df = pd.read_csv(filename)
                
                # Convertir la colonne 'time' en numérique (en place)
                df['time'] = pd.to_numeric(df['time'], errors='coerce')
                
                # Filtrer les données où la puissance est positive
                df = df[df['Power'] > 0]
                
                # Vérification si les colonnes nécessaires existent
                required_columns = ['Power', 'Oxygen', 'Cadence', 'HR', 'RF']
                if all(col in df.columns for col in required_columns):
                    # Parcourir chaque ligne du dataframe
                    for index, row in df.iterrows():
                        for cyclist in cyclists:
                            cyclist_id = cyclist[0]
                            type_test = elem
                            time = row['time']
                            power = row['Power']
                            oxygen = row['Oxygen']
                            cadence = row['Cadence']
                            hr = row['HR']
                            rf = row['RF']

                            # Insérer les données dans la table "test_data"
                            cur.execute("""
                            INSERT INTO test_data (cyclist_id, type_test, time, power, oxygen, cadence, hr, rf)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (cyclist_id, type_test, time, power, oxygen, cadence, hr, rf))
            except Exception as e:
                print(f"Erreur lors de la lecture ou du traitement du fichier {filename}: {e}")
        else:
            print(f"Le fichier {filename} n'existe pas. Passage au test suivant.")

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()
