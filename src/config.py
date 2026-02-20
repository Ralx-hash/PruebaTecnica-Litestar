from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class settings(BaseSettings):
    #declara las variables de entorno para usarlas en la configuracion de la base de datos y JWT
    DATABASE_URL: str = Field(..., env="DATABASE_URL", description= "Credenciales de la BD")
    JWT_KEY: str = Field(..., env = "JWT_KEY", description = "Clave JWT")
    JWT_ALGORITHM: str = Field(..., env = "JWT_ALGORITHM", description = "Algoritmo JWT")

    model_config = SettingsConfigDict(
        env_file=".env", # Busca el archivo .env
        env_file_encoding="utf-8", 
    )

CONFIG = settings()