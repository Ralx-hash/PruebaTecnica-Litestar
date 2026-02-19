from sqlalchemy.ext.asyncio import AsyncSession
from src.database.repositories import UserRepository
from src.database.models import Users

#esto es para proveer el repositorio de usuarios al controlador (DI)
async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(session = db_session)