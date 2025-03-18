from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from auth import hash_password, verify_password, create_token, decode_token
from database import get_db_connection
from datetime import timedelta

app = FastAPI()


# configuration Pydantic pour la création d'un utilisateur
class User(BaseModel):
    username: str
    password: str
    fonction: str # entraineur ou cycliste

# Pydantic pour données de performances

class Performance(BaseModel):
    time : int
    power : int
    oxygen : float
    cadence : int
    HR : float
    RF : float

# authentification
def get_current_user(token : str):
    payload = decode_token(token)
    return {"id": payload["sub"], "fonction": payload["fonction"]}


# incription d’un utilisateur
@app.post("/register") 
def register(user: User):
    conn = get_db_connection()
    hashed_password = hash_password(user.password)
    try:
        conn.execute("INSERT INTO users (username, hashed_password, fonction) VALUES (?, ?, ?)",
                     (user.username, hashed_password, user.fonction))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()
    return {"message": "User created"}


# connexion d’un utilisateur
@app.post("/login")
def login(user: User):
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
    conn.execute("INSERT INTO performances (time, power, oxygen, cadence, HR, RF, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
    ##
    ##
    ##
    ##

    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM performances")