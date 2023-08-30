# Este módulo contiene la configuración y ejecución de la aplicación FastAPI.
from fastapi import FastAPI

# Register routers imports
from app.api.routers.url_routers import router as url_router
from app.api.routers.user_routers import router as user_router


app = FastAPI()
app.title = "api books url".upper()
app.version = "0.1.0"

# Registra las rutas relacionadas con usuarios.
app.include_router(user_router, prefix="/users", tags=["Users"])

# Registra las rutas relacionadas con libros (URLs).
app.include_router(url_router, prefix="/urls", tags=["Urls"])
