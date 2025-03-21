from fastapi import FastAPI, HTTPException, Depends, status
from .auth import hash_password, verify_password, create_token, decode_token
from datetime import timedelta, datetime
import sqlite3
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt

app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# authentification
def get_current_user(token : str = Depends(oauth_scheme)):

    """
    Décoder le token pour récupérer les informations de l'utilisateur courant.
    """
    try:
        payload = decode_token(token)
        print(payload["sub"])
        return {"id": payload["sub"], "fonction": payload["fonction"]}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    



# incription d’un utilisateur
@app.post("/register") 
def register(data: dict):
    """
    Inscription d'un utilisateur.

    Parameters:
        - data (dict): Contient 'cyclist_id', 'username', 'password' et 'fonction'.

    Returns:
        - message (str): Confirmation de la création d'un utilisateur.
    """
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
   
    hashed_password = hash_password(data["password"])

    try:
        conn.execute("INSERT INTO users (cyclist_id, username, password, fonction) VALUES (?, ?, ?, ?)",
                     (data['cyclist_id'],data["username"], hashed_password, data["fonction"]))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()
    return {"message": "User created"}



@app.post("/login")
def login(user: dict):
    """
    Connexion d'un utilisateur et génération d'un token.

    Parameters:
        - user (dict): Contient 'username' et 'password'.

    Returns:
        - access_token (str): Token d'accès pour authentification.
        - token_type (str): Type du token (Bearer).
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Pour que cur.fetchone() retourne un dictionnaire
    cur = conn.cursor()
    # Rechercher l'utilisateur dans la base de données
    user_data = conn.execute("SELECT * FROM users WHERE username = ?", (user["username"],)).fetchone()
    conn.close()
    user_data = dict(user_data)
    if not user_data or not verify_password(user['password'],user_data["password"]):  # 'password' est la colonne dans la base
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Création du token
    print(user_data)
    token = create_token({"sub": str(user_data["id"]), "fonction": user_data["fonction"]}, timedelta(hours=1))
    print("===================",token)
    return {"access_token": token, "token_type": "bearer"}



# Ajout des performances
@app.post("/performances")
def add_performance(performance: dict, current_user: dict = Depends(oauth_scheme)):
    """
    Ajouter une performance pour un cycliste.

    Parameters:
        - performance (dict): Détails de la performance (cyclist_id, vo2max, power, cadence, hr, rf).
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - message (str): Confirmation de l'ajout de la performance.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO tests_data (cyclist_id, vo2max, power, cadence, hr, rf)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (performance["cyclist_id"], performance["vo2max"], performance["power"], 
          performance["cadence"], performance["hr"], performance["rf"]))

    conn.commit()
    conn.close()

    return {"message": "Performance added"}




# visualisation des performances par un entraineur
@app.get("/coach/performances")
def view_performances(current_user: dict = Depends(oauth_scheme)):
    """
    Visualisation des performances par un coach.

    Parameters:
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - result (list): Liste des données de tests.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")
    if current_user["fonction"] != "coach":
        raise HTTPException(status_code=403, detail="acces denied, only coach can access this route")
    
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM test_data")
    result = cur.fetchall()
    return result

# visualisation de l'athele avec le meilleur poids puissance
@app.get("/poidspuissance")
def view_poids_puissance(current_user: dict = Depends(oauth_scheme)):
    """
    Visualisation de l'athlète avec le meilleur rapport poids/puissance.

    Parameters:
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - result (dict): Informations sur l'athlète avec le meilleur ratio.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    

    cur.execute("select name, cyclists.id from cyclists left join tests_data on cyclists.id = cyclist_id group by cyclists.id having weight/power = max(weight/power)")
    result = cur.fetchone()

    conn.close()
    
    return result


# visualisation de l'athele avec la puissance maximale
@app.get("/puissancemax")
def view_poids_puissance(current_user: dict = Depends(oauth_scheme)):
    """
    Visualisation de l'athlète avec la puissance maximale.

    Parameters:
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - result (dict): Informations sur l'athlète ayant la puissance maximale.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    

    cur.execute("""
        SELECT name, id, ppo
        FROM cyclists
        WHERE ppo = (SELECT MAX(ppo) FROM cyclists);
    """)
    result = cur.fetchone()

    return result

# modification de la puissance
@app.put("/modification/{i}/power")
def modifier_power(i: int, power: dict, current_user: dict = Depends(oauth_scheme)):
    """
    Modifier la valeur de puissance pour un test spécifique.

    Parameters:
        - i (int): Identifiant du test.
        - power (dict): Nouvelle valeur de puissance.
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - message (str): Confirmation de la mise à jour.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Mettre à jour uniquement la colonne 'power'
    cur.execute("""
        UPDATE tests_data
        SET power = ?
        WHERE ID = ?
    """, (power['power'], i))

    conn.commit()
    conn.close()

    return {"message": "Power mis à jour avec succès."}


@app.put("/modification/{i}/vo2max")
def modifier_vo2max(i: int, vo2max: dict, current_user: dict = Depends(oauth_scheme)):
    """
    Modifier la valeur de vo2max pour un test spécifique.

    Parameters:
        - i (int): Identifiant du test.
        - power (dict): Nouvelle valeur de vo2max.
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - message (str): Confirmation de la mise à jour.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Mettre à jour uniquement la colonne 'vo2max'
    cur.execute("""
        UPDATE tests_data
        SET vo2max = ?
        WHERE ID = ?
    """, (vo2max['vo2max'], i))

    conn.commit()
    conn.close()

    return {"message": "VO2max mis à jour avec succès."}


@app.put("/modification/{i}/cadence")
def modifier_cadence(i: int, cadence: dict, current_user: dict = Depends(oauth_scheme)):
    """
    Modifier la valeur de cadence pour un test spécifique.

    Parameters:
        - i (int): Identifiant du test.
        - power (dict): Nouvelle valeur de cadence.
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - message (str): Confirmation de la mise à jour.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Mettre à jour uniquement la colonne 'cadence'
    cur.execute("""
        UPDATE tests_data
        SET cadence = ?
        WHERE ID = ?
    """, (cadence['cadence'], i))

    conn.commit()
    conn.close()

    return {"message": "Cadence mis à jour avec succès."}


@app.put("/modification/{i}/hr")
def modifier_hr(i: int, hr: dict, current_user: dict = Depends(oauth_scheme)):
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Mettre à jour uniquement la colonne 'hr'
    cur.execute("""
        UPDATE tests_data
        SET hr = ?
        WHERE ID = ?
    """, (hr['hr'], i))

    conn.commit()
    conn.close()

    return {"message": "HR mis à jour avec succès."}


@app.put("/modification/{i}/rf")
def modifier_rf(i: int, rf: dict, current_user: dict = Depends(oauth_scheme)):
    """
    Modifier la valeur de rf pour un test spécifique.

    Parameters:
        - i (int): Identifiant du test.
        - power (dict): Nouvelle valeur de rf.
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - message (str): Confirmation de la mise à jour.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Mettre à jour uniquement la colonne 'rf'
    cur.execute("""
        UPDATE tests_data
        SET rf = ?
        WHERE ID = ?
    """, (rf['rf'], i))

    conn.commit()
    conn.close()

    return {"message": "RF mis à jour avec succès."}

@app.delete("/supprimer/{i}")
def supprimer_cyclist(i:int, current_user: dict = Depends(oauth_scheme)):
    """
    Supprimer les données d'un cycliste.

    Parameters:
        - i (int): Identifiant du cycliste.
        - current_user (dict): Utilisateur actuellement connecté.

    Returns:
        - message (str): Confirmation de la suppression.
    """
    current_user = decode_token(current_user)
    if current_user["fonction"] not in ["coach"]:
        raise HTTPException(status_code=403, detail="Access denied")

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Mettre à jour uniquement la colonne 'rf'
    cur.execute("""
        DELETE FROM tests_data
        WHERE id = ?
    """, (i,))


    conn.commit()
    conn.close()

    return {"message": f"{i} supprimé avec succès."}
