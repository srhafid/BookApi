# Este módulo contiene la configuración y ejecución de la aplicación FastAPI.
from fastapi import FastAPI
import redis

# Register routers imports
from app.api.routers.url_routers import router as url_router
from app.api.routers.user_routers import router as user_router


app: FastAPI = FastAPI()

# Instancia de Redis para la conexión a la base de datos.
r: redis.Redis = redis.Redis(host="localhost", port=6379, db=0)

# Registra las rutas relacionadas con usuarios.
app.include_router(user_router, prefix="/users", tags=["users"])

# Registra las rutas relacionadas con libros (URLs).
app.include_router(url_router, prefix="/urls", tags=["books"])
