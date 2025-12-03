from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = "cliente"
    
    cliente_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100))
    email = Column(String(100), unique=True)
    envios = relationship("Envio", back_populates="cliente")

class TipoProducto(Base):
    __tablename__ = "tipo_producto"
    tipo_producto_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    envios = relationship("Envio", back_populates="tipo_producto")

class Bodega(Base):
    __tablename__ = "bodega"
    bodega_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255))
    envios_terrestres = relationship("Envio", back_populates="bodega")

class Puerto(Base):
    __tablename__ = "puerto"
    puerto_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(255))
    envios_maritimos = relationship("Envio", back_populates="puerto")

class Envio(Base):
    __tablename__ = "envio"
    envio_id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("cliente.cliente_id"), nullable=False)
    tipo_producto_id = Column(Integer, ForeignKey("tipo_producto.tipo_producto_id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_registro = Column(Date, nullable=False)
    fecha_entrega = Column(Date, nullable=False)
    num_guia = Column(String(10), unique=True, nullable=False)
    tipo_logistica = Column(String(10), nullable=False)
    precio_base = Column(DECIMAL(10, 2), nullable=False)
    descuento_aplicado = Column(DECIMAL(10, 2), nullable=False)
    precio_final = Column(DECIMAL(10, 2), nullable=False)
    # Terrestre
    placa_vehiculo = Column(String(6), nullable=True) 
    bodega_id = Column(Integer, ForeignKey("bodega.bodega_id"), nullable=True) # <-- FK
    # Marítima 
    num_flota = Column(String(8), nullable=True)
    puerto_id = Column(Integer, ForeignKey("puerto.puerto_id"), nullable=True) # <-- FK
    cliente = relationship("Cliente", back_populates="envios")
    tipo_producto = relationship("TipoProducto", back_populates="envios")
    bodega = relationship("Bodega", back_populates="envios_terrestres", foreign_keys=[bodega_id])
    puerto = relationship("Puerto", back_populates="envios_maritimos", foreign_keys=[puerto_id])