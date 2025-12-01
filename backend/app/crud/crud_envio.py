from sqlalchemy.orm import Session
from ..database import models
from ..schemas import envio_schema
import uuid

def generar_numero_guia():
    # Genera cod 10 dijitos
    return str(uuid.uuid4()).replace('-', '')[:10].upper()

def calcular_descuento(precio_base: float, cantidad: int, tipo_logistica: str):
    """Calcula los precios finales con el descuento del 5% o 3% si cantidad > 10."""
    descuento_porcentaje = 0.0
    
    if cantidad > 10:
        if tipo_logistica == 'Terrestre':
            descuento_porcentaje = 0.05
        elif tipo_logistica == 'Maritimo':
            descuento_porcentaje = 0.03
        
    descuento_aplicado = round(precio_base * descuento_porcentaje, 2)
    precio_final = round(precio_base - descuento_aplicado, 2)
    
    return precio_final, descuento_aplicado

def create_envio_terrestre(db: Session, envio: envio_schema.EnvioTerrestreCreate):
    
    precio_final, descuento_aplicado = calcular_descuento(
        envio.precio_envio, envio.cantidad, "Terrestre"
    )
    
    db_envio = models.Envio(
        **envio.model_dump(exclude_unset=True), # Toma todos los campos de Pydantic
        tipo_logistica="Terrestre",
        precio_base=envio.precio_envio,
        descuento_aplicado=descuento_aplicado,
        precio_final=precio_final,
        num_guia=generar_numero_guia(),
        num_flota=None, 
        puerto_id=None
    )
    
    db.add(db_envio)
    db.commit()
    db.refresh(db_envio)
    return db_envio

def create_envio_maritimo(db: Session, envio: envio_schema.EnvioMaritimoCreate) -> models.Envio:
    """Crea y persiste un nuevo envío marítimo."""

    precio_final, descuento_aplicado = calcular_descuento(
        envio.precio_envio, envio.cantidad, "Maritimo"
    )
    
    db_envio = models.Envio(

        **envio.model_dump(exclude_unset=True), 
        
        tipo_logistica="Maritimo",
        precio_base=envio.precio_envio,
        descuento_aplicado=descuento_aplicado,
        precio_final=precio_final,
        num_guia=generar_numero_guia(),

        placa_vehiculo=None, 
        bodega_id=None
    )
    
    db.add(db_envio)
    db.commit()
    db.refresh(db_envio)
    return db_envio

def get_envios_by_filter(db: Session, num_guia: str | None = None, tipo_logistica: str | None = None):
    """Implementación de la consulta con filtros."""
    query = db.query(models.Envio)
    
    if num_guia:
        query = query.filter(models.Envio.num_guia == num_guia)
    
    if tipo_logistica:
        query = query.filter(models.Envio.tipo_logistica == tipo_logistica)
        
    return query.all()