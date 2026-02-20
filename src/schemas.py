from dataclasses import dataclass
from pydantic import BaseModel, Field

#DTO'S

@dataclass
class UsuarioBase:
    id: int
    nombre: str
    rol: str
    renta_mensual: float


@dataclass
class UsuarioCreate:
    nombre: str
    rol: str
    renta_mensual: float
    email: str
    normalized_email: str
    hashed_password: str

#dataclass me estaba dando problemas para ingresarlo datos en el body
class UsuarioLogin(BaseModel):
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Email del usuario") 
    password: str
