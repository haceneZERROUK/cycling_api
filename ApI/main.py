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
    try:
        payload = decode_token(token)
        print(payload["sub"])
        return {"id": payload["sub"], "fonction": payload["fonction"]}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    



# incription d’un utilisateur
@app.post("/register") 
def register(data: dict):
    
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
    current_user = decode_token(current_user)
    print(current_user)
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


# # suppression d’une performance par un cycliste
# @app.delete("/performances/{performance_id}")
# def delete_performance(performance_id: int, token: str = Depends(get_current_user)):
#     current_user = get_current_user(token)
#     if current_user["fonction"] != "cyclist":
#         raise HTTPException(status_code=403, detail="acces denied")
    
#     conn = get_db_connection()
#     conn.execute("DELETE FROM performances WHERE id = ? AND user_id = ?", (performance_id, current_user["id"]))
#     conn.commit()
#     conn.close()
#     return {"message": "Performance deleted"}


# # visualisation des performances par un entraineur
# @app.get("/coach/performances")
# def view_performances(token: str = Depends(get_current_user)):
#     current_user = get_current_user(token)
#     if current_user["fonction"] != "coach":
#         raise HTTPException(status_code=403, detail="acces denied, only coach can access this route")
    
#     #connexion a la base de données pour obtenir les performances
    

#     conn = get_db_connection()
#     cursor = conn.execute("SELECT * FROM performances"
#     #
#     #
#     #
#     #
#     #

#     performances = cursor.fetchall()
#     conn.close()

#     # Mise en forme des données pour les retourner
#     return {"performances": [dict(performance) for performance in performances]}

   
   
#      cursor = conn.execute("""
#      SELECT p.id AS performance_id, 
#             p.athlete_id, 
#             u.username AS cyclist_name, 
#             p.time,
#             p.power,
#             p.oxygen,
#             p.cadence,
#             p.HR,
#             p.RF, 
#             p.test_date
#      FROM performances p
#      INNER JOIN users u ON p.cyclist_id = u.id
#     """)

# #     # Entraîneurs : Modifier une performance
# # @app.put("/coach/performances/{performance_id}")
# # def update_performance(performance_id: int, performance: Performance, token: str = Depends(get_current_user)):
# #     current_user = get_current_user(token)
# #     if current_user["role"] != "coach":
# #         raise HTTPException(status_code=403, detail="acces denied")

# #     conn = get_db_connection()
# #     conn.execute("""
# #     UPDATE performances
# #     SET time = ?, power = ?, oxygen = ?, cadence = ?, HR = ?, RF = ?, test_date = ?
# #     WHERE id = ?
# #     """, (performance.time, performance.power, performance.oxygene, performance.cadence, performance.HR, performance.RF, performance.test_date, performance_id))
# #     conn.commit()
# #     conn.close()
# #     return {"message": "Performance updated by coach"}

# # Entraîneurs : Supprimer une performance
# @app.delete("/coach/performances/{performance_id}")
# def delete_performance_as_coach(performance_id: int, token: str = Depends(get_current_user)):
#     current_user = get_current_user(token)
#     if current_user["role"] != "coach":
#         raise HTTPException(status_code=403, detail="acces denied")

#     conn = get_db_connection()
#     conn.execute("DELETE FROM performances WHERE id = ?", (performance_id,))
#     conn.commit()
#     conn.close()
#     return {"message": "Performance deleted by coach"}