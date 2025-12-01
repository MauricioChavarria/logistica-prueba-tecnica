from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.security import get_current_user
from ...database.database import get_db
from ...schemas import envio_schema
from ...crud import crud_envio

router = APIRouter(
    prefix="/terrestre",
    tags=["Logística Terrestre"],
    dependencies=[Depends(get_current_user)] 
)

@router.post("/envios", response_model=envio_schema.EnvioResponse, status_code=201)
def create_terrestrial_delivery(
    envio: envio_schema.EnvioTerrestreCreate, 
    db: Session = Depends(get_db)
):
    try:
        db_envio = crud_envio.create_envio_terrestre(db=db, envio=envio)
        return db_envio
    except Exception as e:
        # Error
        raise HTTPException(status_code=400, detail=f"Error al crear envío: {e}")

@router.get("/envios", response_model=List[envio_schema.EnvioResponse])
def get_terrestrial_deliveries(
    num_guia: Optional[str] = None,
    db: Session = Depends(get_db)
):
    envios = crud_envio.get_envios_by_filter(db, num_guia=num_guia, tipo_logistica="Terrestre")
    return envios