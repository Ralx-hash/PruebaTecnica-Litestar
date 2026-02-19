from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.config.cors import CORSConfig
from src.database.setup import sql_plugin
from src.controllers.userController import userController

route_handlers = [userController] #aun sin existir userController

openapi_config = OpenAPIConfig(
    title="My API",
    version="1.0.0",
)

cors_config = CORSConfig(
    allow_origins=["*"],  # Permite todos los orígenes
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
    expose_headers=["Authorization", "Content-Type"],  # Expone headers al frontend
    allow_credentials=False,  # No permite credenciales con allow_origins=["*"]
) 

app = Litestar(
    route_handlers=route_handlers,
    plugins = [sql_plugin],
    cors_config=cors_config)

