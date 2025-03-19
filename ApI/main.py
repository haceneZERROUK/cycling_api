from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from auth import hash_password, verify_password, create_token, decode_token
from database import get_db_connection
from datetime import timedelta
import sqlite3

app = FastAPI()


# # configuration Pydantic pour la création d'un utilisateur
# class User(BaseModel):
#     username: str
#     password: str
#     fonction: str # coach or cyclist

conn = sqlite3.connect('database.db')
cur = conn.cursor()



cur.execute("""
INSERT INTO cyclist (name, gender, age, weight, height, vo2max, ppo, p1, p2, p3)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", cyclist)


conn.commit()
conn.close()

# authentification
def get_current_user(token : str):
    payload = decode_token(token)
    return {"id": payload["sub"], "fonction": payload["fonction"]}


# incription d’un utilisateur
@app.post("/register") 
def register(data: dict):

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
   
    hashed_password = hash_password(data["password"])
    try:
        conn.execute("INSERT INTO users (username, cyclist_id hashed_password, fonction) VALUES (?, ?, ?)",
                     (data["username"], hashed_password, data["fonction"]))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()
    return {"message": "User created"}


# connexion d’un utilisateur
@app.post("/login")
def login(user):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    user_data = cursor.fetchone()
    conn.close()
    if not user_data or not verify_password(user.password, user_data["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token({"sub": user_data["id"], "fonction": user_data["fonction"]}, timedelta(hours=1))
    return {"acces_token": token, "token_type": "bearer"}

# ajour d’une performance par un cycliste
@app.post("/performances")
def add_performance(performance: Performance, token: str = Depends(get_current_user)):
    current_user = get_current_user(token)
    if current_user["fonction"] != "cyclist":
        raise HTTPException(status_code=403, detail="acces denied")
    conn = get_db_connection()
    conn.execute("INSERT INTO performances (time, Power, Oxygen, Cadence, HR, RF, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                 (performance.time, performance.power, performance.oxygen, performance.cadence, performance.HR, performance.RF, current_user["id"]))
    conn.commit()
    conn.close()
    return {"message": "Performance added"}


# suppression d’une performance par un cycliste
@app.delete("/performances/{performance_id}")
def delete_performance(performance_id: int, token: str = Depends(get_current_user)):
    current_user = get_current_user(token)
    if current_user["fonction"] != "cyclist":
        raise HTTPException(status_code=403, detail="acces denied")
    
    conn = get_db_connection()
    conn.execute("DELETE FROM performances WHERE id = ? AND user_id = ?", (performance_id, current_user["id"]))
    conn.commit()
    conn.close()
    return {"message": "Performance deleted"}


# visualisation des performances par un entraineur
@app.get("/coach/performances")
def view_performances(token: str = Depends(get_current_user)):
    current_user = get_current_user(token)
    if current_user["fonction"] != "coach":
        raise HTTPException(status_code=403, detail="acces denied, only coach can access this route")
    
    #connexion a la base de données pour obtenir les performances
    

    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM performances"
    #
    #
    #
    #
    #

    performances = cursor.fetchall()
    conn.close()

    # Mise en forme des données pour les retourner
    return {"performances": [dict(performance) for performance in performances]}

   
   
     cursor = conn.execute("""
     SELECT p.id AS performance_id, 
            p.athlete_id, 
            u.username AS cyclist_name, 
            p.time,
            p.power,
            p.oxygen,
            p.cadence,
            p.HR,
            p.RF, 
            p.test_date
     FROM performances p
     INNER JOIN users u ON p.cyclist_id = u.id
    """)

    # Entraîneurs : Modifier une performance
@app.put("/coach/performances/{performance_id}")
def update_performance(performance_id: int, performance: Performance, token: str = Depends(get_current_user)):
    current_user = get_current_user(token)
    if current_user["role"] != "coach":
        raise HTTPException(status_code=403, detail="acces denied")

    conn = get_db_connection()
    conn.execute("""
    UPDATE performances
    SET time = ?, power = ?, oxygen = ?, cadence = ?, HR = ?, RF = ?, test_date = ?
    WHERE id = ?
    """, (performance.time, performance.power, performance.oxygene, performance.cadence, performance.HR, performance.RF, performance.test_date, performance_id))
    conn.commit()
    conn.close()
    return {"message": "Performance updated by coach"}

# Entraîneurs : Supprimer une performance
@app.delete("/coach/performances/{performance_id}")
def delete_performance_as_coach(performance_id: int, token: str = Depends(get_current_user)):
    current_user = get_current_user(token)
    if current_user["role"] != "coach":
        raise HTTPException(status_code=403, detail="acces denied")

    conn = get_db_connection()
    conn.execute("DELETE FROM performances WHERE id = ?", (performance_id,))
    conn.commit()
    conn.close()
    return {"message": "Performance deleted by coach"}