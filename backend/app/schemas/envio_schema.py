from pydantic import BaseModel, Field
from datetime import date

class EnvioBase(BaseModel):
    cliente_id: int
    tipo_producto_id: int
    cantidad: int = Field(..., gt=0)
    fecha_registro: date
    fecha_entrega: date
    precio_envio: float = Field(..., gt=0.0)

class EnvioTerrestreCreate(EnvioBase):
    bodega_id: int
    placa_vehiculo: str = Field(..., pattern=r"^[A-Z]{3}\d{3}$") 

class EnvioMaritimoCreate(EnvioBase):
    puerto_id: int
    num_flota: str = Field(..., pattern=r"^[A-Z]{3}\d{4}[A-Z]{1}$")

class EnvioResponse(BaseModel):
    envio_id: int
    num_guia: str
    precio_base: float
    descuento_aplicado: float
    precio_final: float
    tipo_logistica: str
    placa_vehiculo: str | None = None
    bodega_id: int | None = None
    num_flota: str | None = None
    puerto_id: int | None = None

    class Config:
        from_attributes = True


# Alias por compatibilidad histórica / tests que usan otro nombre
EnvioOut = EnvioResponse