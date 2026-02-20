from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.config.cors import CORSConfig
from src.database.setup import sql_plugin
from src.controllers.userController import userController

route_handlers = [userController]


cors_config = CORSConfig(
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
    expose_headers=["Authorization", "Content-Type"],  
    allow_credentials=False,  
) 

app = Litestar(
    route_handlers=route_handlers,
    plugins = [sql_plugin],
    cors_config=cors_config)

