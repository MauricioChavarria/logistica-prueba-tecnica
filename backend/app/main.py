from fastapi import FastAPI
from .api.api import api_router

app = FastAPI(
    title="Logística Terrestre y Marítima API",
    description="API RESTful para la gestión de envíos de transporte.",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "API de Logística en funcionamiento. Ver /docs para la documentación."}