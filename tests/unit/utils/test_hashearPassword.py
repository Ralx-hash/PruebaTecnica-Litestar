import pytest
from src.utils.hashearPassword import hash_password


def test_hash_password_devuelve_hash_diferente():

    # PREPARAR 
    password_original = "MiPassword123"
    
    
    # EJECUTAR
    password_hasheada = hash_password(password_original)
    
    
    # VERIFICAR 
    assert password_hasheada != password_original, \
        "El hash debe ser diferente al original"
    
    assert isinstance(password_hasheada, str), \
        "El hash debe ser un string"
    
    password_hasheada_2 = hash_password(password_original)
    assert password_hasheada != password_hasheada_2, \
        "Cada hash debe ser diferente (bcrypt usa salt aleatorio)"
