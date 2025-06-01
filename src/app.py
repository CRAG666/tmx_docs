import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config.exception_handler import CustomException
from src.config.base import create_db_and_tables
from src.entities.user.routes import user_controller, user_role_controller
from src.entities.state.routes import state_controller
from src.entities.device.routes import device_controller
from src.entities.device.routes import device_relation_controller
from .services.security import DecryptionMiddleware, EncryptionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


key = os.urandom(32)  # Clave AES-256 (32 bytes)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="REST API Example",
    description="API REST con FastAPI y SQLite usando Repository Pattern",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middlewares en el orden correcto
app.add_middleware(DecryptionMiddleware, key=key)
app.add_middleware(EncryptionMiddleware, key=key)


# Manejo de excepciones
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})


# Ruta principal
@app.get("/")
async def root():
    return {
        "message": "API REST con FastAPI y SQLite",
        "documentation": "/docs",
        "repository_pattern": True,
    }


# Registro de routers
user_controller.register_routes(app)
user_role_controller.register_routes(app)
state_controller.register_routes(app)
device_controller.register_routes(app)
device_relation_controller.register_routes(app)


@app.get("/test")
async def test_endpoint():
    return {"message": "Datos recibidos"}


# Punto de entrada para ejecución directa
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run("app:app", host=host, port=port, reload=True)
