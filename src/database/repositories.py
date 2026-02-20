from litestar.plugins.sqlalchemy import repository
from sqlalchemy import select

from src.database.models import Users 
from src.schemas import UsuarioCreate

#logica para el acceso de datos
class UserRepository(repository.SQLAlchemyAsyncRepository[Users]):
    model_type = Users

    async def agregar_usuarios_masivo(self, usuarios: list[UsuarioCreate]) -> list[Users]:
        try:
            nuevos_usuarios = []

            for usuario in usuarios:

                usuario_dict = {
                    'nombre': usuario.nombre,
                    'rol': usuario.rol, 
                    'renta_mensual': usuario.renta_mensual,
                    'email': usuario.email,
                    'normalized_email': usuario.normalized_email,
                    'hashed_password': usuario.hashed_password
                }
                nuevo_usuario = self.model_type(**usuario_dict)
                nuevos_usuarios.append(nuevo_usuario)
            
            self.session.add_all(nuevos_usuarios)
            await self.session.commit()
                
            return nuevos_usuarios
            
        except Exception as e:
            # Rollback en caso de error
            await self.session.rollback()
            raise e


        # Agregar a src/database/repositories.py
    async def obtener_usuarios_por_roles(self, rolUsuario: str, userId: int) -> list[Users]:
        # Obtener el rol del usuario que hace la petición
        
        if rolUsuario == "admin":
            # Admin ve todos
            result = await self.session.execute(select(Users))
            return result.scalars().all()

        elif rolUsuario == "supervisor":
            # Supervisor ve usuarios y supervisores
            result = await self.session.execute(
                select(Users).where(Users.rol.in_(["usuario", "supervisor"]))
            )
            return result.scalars().all()

        elif rolUsuario == "usuario":
            # Usuario solo ve usuarios (incluyendo él mismo)
            result = await self.session.execute(
                select(Users).where(Users.id == userId)
            )
            return result.scalars().all()

        return []


    async def usuario_existe(self, email: str) -> bool:
        result = await self.session.execute(select(Users).where(Users.email == email))
        return result.scalars().first() is not None

    # if requesting_user_role == "admin":
    #     # Admin ve todos
    #     result = await self.session.execute(select(Users))
    #     return result.scalars().all()
    
    # elif requesting_user_role == "supervisor":
    #     # Supervisor ve usuarios y supervisores
    #     result = await self.session.execute(
    #         select(Users).where(Users.rol.in_(["usuario", "supervisor"]))
    #     )
    #     return result.scalars().all()
    
    # elif requesting_user_role == "usuario":
    #     # Usuario solo ve su propio perfil
    #     if not requesting_user_id:
    #         raise ValueError("Se requiere user_id para usuarios")
    #     result = await self.session.execute(
    #         select(Users).where(Users.id == requesting_user_id)
    #     )
    #     return [result.scalars().first()]
    
    # else:
    #     raise ValueError(f"Rol no reconocido: {requesting_user_role}")