from passlib.hash import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# chargement de la secret key via le fichier .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


# Fonction de hashage de mot de passe
def hash_password(password: str) -> str: 
    return bcrypt.hash(password)

# Fonction de vérification de mot de passe
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)


# fonction de création des tokens
def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.uctnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# fonction de decryptage des tokens
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    

    