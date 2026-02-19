from advanced_alchemy.extensions.litestar import (SQLAlchemyInitPlugin, SQLAlchemyAsyncConfig,
    AsyncSessionConfig)

from src.config import CONFIG

#esto es para no borrar los datos cada vez que se hace un commit
session_config = AsyncSessionConfig(expire_on_commit=False)

#configuracion del plugin para la sesion asincrona
sql_config = SQLAlchemyAsyncConfig(
    connection_string = CONFIG.DATABASE_URL,
    session_config = session_config,
)

#esto se pasa para app.py para inicializar el plugin de SQLAlchemy 
sql_plugin = SQLAlchemyInitPlugin(config = sql_config)