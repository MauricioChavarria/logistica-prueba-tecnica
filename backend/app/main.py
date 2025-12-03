from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.api import api_router
from fastapi import Request

app = FastAPI(
    title="Logística Terrestre y Marítima API",
    description="API RESTful para la gestión de envíos de transporte.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://shiny-space-enigma-9jw9w7qr7wwfppqq-5173.app.github.dev",
        "https://shiny-space-enigma-9jw9w7qr7wwfppqq-5174.app.github.dev",
    ],
    allow_origin_regex=r".*app\.github\.dev",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/debug-headers")
async def debug_headers(request: Request):
    """Endpoint de diagnóstico que devuelve los encabezados de la petición."""
    return {k: v for k, v in request.headers.items()}

@app.get("/")
def read_root():
    return {"message": "API de Logística en funcionamiento. Ver /docs para la documentación."}