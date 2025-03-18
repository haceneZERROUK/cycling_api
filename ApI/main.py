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

