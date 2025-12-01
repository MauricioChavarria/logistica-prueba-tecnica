from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.security import get_current_user
from ...database.database import get_db
from ...schemas import envio_schema
from ...crud import crud_envio

router = APIRouter(
    prefix="/maritimo",
    tags=["Logística Marítima"],
    dependencies=[Depends(get_current_user)] 
)

@router.post("/envios", response_model=envio_schema.EnvioResponse, status_code=201)
def create_maritime_delivery(
    envio: envio_schema.EnvioMaritimoCreate,  # <-- Usa el Schema Marítimo
    db: Session = Depends(get_db)
):
    """Crea un nuevo registro de envío marítimo aplicando el descuento del 3% si es aplicable."""
    try:
        db_envio = crud_envio.create_envio_maritimo(db=db, envio=envio)
        return db_envio
    except Exception as e:
        # errores
        raise HTTPException(status_code=400, detail=f"Error al crear envío marítimo: {e}")

@router.get("/envios", response_model=List[envio_schema.EnvioResponse])
def get_maritime_deliveries(
    num_guia: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Consulta envíos marítimos, con opción de filtrar por número de guía."""
    envios = crud_envio.get_envios_by_filter(db, num_guia=num_guia, tipo_logistica="Maritimo")
    return envios