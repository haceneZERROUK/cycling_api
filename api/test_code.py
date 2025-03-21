from datetime import timedelta
from auth import hash_password, verify_password, create_token, decode_token

# Tester le hashage du mot de passe
password = "monSuperMotDePasse"
hashed = hash_password(password)
print("Hashed Password:", hashed)

# Vérifier le mot de passe
is_valid = verify_password(password, hashed)
print("Password Valid:", is_valid)

# Tester la création de token
data = {"user_id": 123}
expires = timedelta(minutes=15)
token = create_token(data, expires)
print("Generated Token:", token)

# Tester le décryptage du token
try:
    decoded = decode_token(token)
    print("Decoded Token:", decoded)
except Exception as e:
    print("Error:", e)
