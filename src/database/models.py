from advanced_alchemy.base import BigIntBase
from sqlalchemy.dialects.postgresql import VARCHAR, NUMERIC
from sqlalchemy.orm import Mapped, mapped_column

class Users(BigIntBase):
    __tablename__ = "users"

    #mapeo las columnas a su simil de postgresql
    nombre: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    rol: Mapped[str] = mapped_column(VARCHAR(50))
    renta_mensual: Mapped[float] = mapped_column(NUMERIC(12, 2), default=0.00)
    email: Mapped[str] = mapped_column(VARCHAR(255))
    normalized_email: Mapped[str] = mapped_column(VARCHAR(255))
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255))


    #esto es para debuggear
    def __repr__(self) -> str:
        return f"User(id={self.id}, nombre='{self.nombre}', rol='{self.rol}', renta_mensual={self.renta_mensual})"

    #esto es para enviar la peticion http al momento de enviar la lista de usuarios
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rol": self.rol,
            "renta_mensual": float(self.renta_mensual) if self.renta_mensual is not None else None,
            "email": self.email
        }