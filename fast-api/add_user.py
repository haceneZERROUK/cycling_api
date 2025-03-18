import sqlite3

# Connexion à la base de données


conn = sqlite3.connect('../database.db')
cur = conn.cursor()

# Sélectionner tous les cyclistes de la table "cyclist"
cur.execute("SELECT id FROM cyclist")
cyclists = cur.fetchall()

# Ajouter un utilisateur pour chaque cycliste
for cyclist in cyclists:
    cyclist_id = cyclist[0]
    username = f"user_{cyclist_id}"  # Générer le nom d'utilisateur sous la forme user_<id>
    password = "azerty"  # Le mot de passe est toujours 'azerty'
    
    # Insérer l'utilisateur dans la table "user"
    cur.execute("""
    INSERT INTO user (cyclist_id, username, password)
    VALUES (?, ?, ?)
    """, (cyclist_id, username, password))

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()