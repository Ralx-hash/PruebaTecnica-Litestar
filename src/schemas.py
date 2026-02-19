from dataclasses import dataclass, field
from pydantic import BaseModel

#DTO'S

@dataclass
class UsuarioBase:
    id: int
    nombre: str
    rol: str
    renta_mensual: float


#esto va a ser para ingresar el json que tengo
@dataclass
class UsuarioCreate:
    nombre: str
    rol: str
    renta_mensual: float
    email: str
    normalized_email: str
    hashed_password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str
