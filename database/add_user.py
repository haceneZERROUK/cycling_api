import sqlite3
import hashlib
# Connexion à la base de données


conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Sélectionner tous les cyclistes de la table "cyclist"
cur.execute("SELECT id FROM cyclists")
cyclists = cur.fetchall()

# Ajouter un compte utilisateur pour chaque cycliste
for cyclist in cyclists:
    cyclist_id = cyclist[0]
    username = f"user_{cyclist_id}"  # Générer le nom d'utilisateur sous la forme user_<id>
    mdp = 'azerty'
    password = hashlib.sha256(mdp.encode('utf-8')).hexdigest()  # Le mot de passe est toujours 'azerty'
    fonction = "cyclist"  # fonction de l’utilisateur
    

    # Insérer l'utilisateur dans la table "user"
    cur.execute("""
    INSERT INTO users (cyclist_id, username, password, fonction)
    VALUES (?, ?, ?, ?)
    """, (cyclist_id, username, password, fonction))

# ajouter un compte utilisateur pour l’entraineur

cyclist_id = None # pas d’association avec cycliste
username = "coach1" # nom d’utilisateur de l’entraineur 
mdp = "azerty" # mot de passe de l’entraineur
password = hashlib.sha256(mdp.encode('utf-8')).hexdigest()  # Le mot de passe est toujours 'azerty'
fonction = "coach"  # fonction de l’utilisateur

cur.execute("""
    INSERT INTO users (cyclist_id, username, password, fonction)
    VALUES (?, ?, ?, ?)
    """, (cyclist_id, username, password, fonction))

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()