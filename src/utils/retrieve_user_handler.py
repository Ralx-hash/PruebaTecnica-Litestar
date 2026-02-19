from litestar.connection import ASGIConnection
from litestar.security.jwt import Token
from ..database.models import Users
from ..database.repositories import UserRepository
from sqlalchemy import select
import logging

logger = logging.getLogger(__name__)


# Esto es un handler para obtener al usuario autenticado a partid de su JWT
# Es necesario tener esto para poder configurar JWTAuth
async def retrieve_user_handler(token: Token, connection: ASGIConnection) -> Users | None:
    try:
        user_id = int(token.sub)
      
        # trae la sesion de sqlalchemy del estado de la app
        app = connection.scope["app"]
        session_maker = app.state.session_maker_class
        
        async with session_maker() as db_session:
            #traer el repositorio de usuarios para hacer la consulta a la base de datos
            user_repo = UserRepository(session=db_session)
            
            stmt = select(Users).where(Users.id == user_id)
            result = await user_repo.session.execute(stmt)
            user = result.scalars().first()
            
            if user:
                return user
            else:
                return None
                
    except ValueError:
        logger.error(f"ID de usuario inválido en token: {token.sub}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado en auth handler: {e}")
        logger.exception("Detalles completos del error:")
        return None