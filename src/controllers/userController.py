from litestar import Controller, post, get, delete, put, Request
from litestar.params import Body
from litestar.exceptions import HTTPException
from litestar.connection import ASGIConnection
from sqlalchemy import select
from litestar.di import Provide
from litestar.security.jwt import JWTAuth, Token
from src.database.dependencies import provide_user_repo
from src.utils.retrieve_user_handler import retrieve_user_handler
from src.database.repositories import UserRepository
from src.database.models import Users
from src.schemas import UsuarioCreate, UsuarioLogin
from src.utils.hashearPassword import hash_password, verify_password
from src.config import CONFIG
from datetime import timedelta, datetime, timezone

jwt_auth = JWTAuth[Users](
    token_secret=CONFIG.JWT_KEY,
    algorithm=CONFIG.JWT_ALGORITHM,
    default_token_expiration=timedelta(hours=1),
    retrieve_user_handler=retrieve_user_handler,
    exclude = ["/login", "/register", "/openapi.json", "/docs", "/redoc", "/schema"]
)

class userController(Controller):
    path = "/users"
    dependencies = {"user_repo": Provide(provide_user_repo)}

    @get("/all-dict") #configurar esto para recibir middleware de JWTAuth
    async def get_all_users_dict(self, user_repo: UserRepository) -> list[dict]:
        try:
            result = await user_repo.session.execute(select(Users))
            users = result.scalars().all()
            users_dict = [user.to_dict() for user in users]
            return users_dict
        except Exception as e:
            print(f"Error en get_all_users_dict: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor al obtener usuarios")


    #agrega usuarios desde un array de objetos, sin ids
    @post("/agregar-masivo")
    async def agregar_usuarios_masivo(self, data: list[dict], user_repo: UserRepository) -> dict:
        try:
            usuarios = data
            usuarios_crear = []
            campos_validos = {'nombre', 'rol', 'renta_mensual'}
            
            for usuario_data in usuarios:
                # Filtrar solo los campos que existen en UsuarioCreate
                datos_filtrados = {k: v for k, v in usuario_data.items() if k in campos_validos}
                
                # Generar email automáticamente basado en el nombre
                if 'nombre' in datos_filtrados:
                    nombre_sin_espacios = datos_filtrados['nombre'].replace(' ', '')
                    datos_filtrados['email'] = f"{nombre_sin_espacios}@gmail.com"
                    datos_filtrados['normalized_email'] = f"{nombre_sin_espacios.upper()}@gmail.com"
                    datos_filtrados['hashed_password'] = hash_password(datos_filtrados['email'])

                
                print(f"Datos filtrados para usuario: {datos_filtrados}")
                
                # Validar que tenga los campos requeridos
                if not all(campo in datos_filtrados for campo in campos_validos):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Faltan campos requeridos en usuario: {usuario_data}. Requeridos: {campos_validos}"
                    )
                
            #     # Crear el objeto UsuarioCreate
                usuario_create = UsuarioCreate(**datos_filtrados)
                usuarios_crear.append(usuario_create)
            
            # Hacer el insert masivo usando el repositorio
            nuevos_usuarios = await user_repo.agregar_usuarios_masivo(usuarios_crear)
            
            return {
                "mensaje": f"Se insertaron {len(nuevos_usuarios)} usuarios correctamente",
                "total_insertados": len(nuevos_usuarios),
                "usuarios_procesados": len(usuarios)
            }
            
        except Exception as e:
            print(f"Error en agregar_usuarios_masivo: {e}")
            raise HTTPException(status_code=500, detail="Error interno del servidor al agregar usuarios")
        
    
    @post("/login")  
    async def login(self, data: UsuarioLogin, user_repo: UserRepository) -> dict:
        try:
            stmt = await user_repo.session.execute(select(Users).where(Users.email == data.email))
            user = stmt.scalars().first()

            if not user:
                raise HTTPException(status_code=401, detail="Email no encontrado")


            validate_password = verify_password(data.password, user.hashed_password)

            if not validate_password:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")

            # Generar el token JWT
            token = jwt_auth.create_token(
                identifier=str(user.id),
                token_extras={"email": user.email, "rol": user.rol}
            )

            expiration_time = datetime.now(timezone.utc) + jwt_auth.default_token_expiration

            # Crear la respuesta completa con token y datos del usuario(cambiar esto)
            return {
                "access_token": token,
                "token_type": "bearer",
                "expiration": expiration_time.isoformat(),
            }

        except Exception as e:
            print(f"Error en login: {e}")
            raise



    @get("/users-filtered", middleware=[jwt_auth.middleware])
    async def obtener_usuarios_por_rol(self, user_repo: UserRepository, request: Request) -> dict:
        try:
            # Acceder al usuario a través del request scope
            current_user = request.scope.get("user")
            
            if not current_user:
                raise HTTPException(status_code=401, detail="Usuario no autenticado")
            
            user_rol = current_user.rol
            user_id = current_user.id

            if not await user_repo.usuario_existe(current_user.email):
                raise HTTPException(status_code=401, detail="Usuario no encontrado")

            lista_usuarios = await user_repo.obtener_usuarios_por_roles(user_rol, user_id)
            
            if lista_usuarios is None:
                return []
            
            return [usuario.to_dict() for usuario in lista_usuarios]

            
        except Exception as e:
            print(f"Error en obtener_usuarios_por_rol: {e}")
            raise e

    @get("/perfil", middleware=[jwt_auth.middleware])
    async def obtener_perfil(self, request: Request) -> dict:
        try:
            current_user = request.scope.get("user")
            
            if not current_user:
                raise HTTPException(status_code=401, detail="Usuario no autenticado")
            
            return current_user.to_dict()
        
        except Exception as e:
            print(f"Error en obtener_perfil: {e}")
            raise e