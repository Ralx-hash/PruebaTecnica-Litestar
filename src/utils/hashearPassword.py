import bcrypt

def hash_password(password: str) -> str:
    # Hashea una contraseña
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed: str) -> bool:
    #Verifica la contraseña con el hash de la bd
    return bcrypt.checkpw(plain_password.encode(), hashed.encode())