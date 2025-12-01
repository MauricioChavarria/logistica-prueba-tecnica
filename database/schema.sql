CREATE TABLE Cliente (
    cliente_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Tipo_Producto (
    tipo_producto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Bodega (
    bodega_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255)
)

CREATE TABLE Puerto (
    puerto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(255)
);

CREATE TABLE Envio (
    envio_id SERIAL PRIMARY KEY,
    
    cliente_id INT NOT NULL REFERENCES Cliente(cliente_id),
    tipo_producto_id INT NOT NULL REFERENCES Tipo_Producto(tipo_producto_id),
    
    cantidad INT NOT NULL CHECK (cantidad > 0),
    fecha_registro DATE NOT NULL,
    fecha_entrega DATE NOT NULL CHECK (fecha_entrega >= fecha_registro),

    --GUIA
    num_guia CHAR(10) UNIQUE NOT NULL,
    CONSTRAINT chk_num_guia_format CHECK (num_guia ~ '^[A-Z0-9]{10}$'),
    
    tipo_logistica VARCHAR(10) NOT NULL 
        CHECK (tipo_logistica IN ('Terrestre', 'Maritimo')),

    precio_base DECIMAL(10, 2) NOT NULL CHECK (precio_base >= 0),
    descuento_aplicado DECIMAL(10, 2) NOT NULL CHECK (descuento_aplicado >= 0),
    precio_final DECIMAL(10, 2) NOT NULL CHECK (precio_final >= 0),
    
    -- TERRESTRE
    placa_vehiculo CHAR(6), 
    bodega_id INT REFERENCES Bodega(bodega_id),
    -- Validacion (AAA999)
    CONSTRAINT chk_placa_format CHECK (placa_vehiculo ~ '^[A-Z]{3}[0-9]{3}$'),

    -- MARITIMA
    num_flota CHAR(8),
    puerto_id INT REFERENCES Puerto(puerto_id),
    -- Validacion (AAA9999A)
    CONSTRAINT chk_flota_format CHECK (num_flota ~ '^[A-Z]{3}[0-9]{4}[A-Z]{1}$'),

  
    CONSTRAINT chk_logistica_fields CHECK (
        (tipo_logistica = 'Terrestre' AND placa_vehiculo IS NOT NULL AND bodega_id IS NOT NULL AND num_flota IS NULL AND puerto_id IS NULL) OR
        (tipo_logistica = 'Maritimo' AND num_flota IS NOT NULL AND puerto_id IS NOT NULL AND placa_vehiculo IS NULL AND bodega_id IS NULL)
    )
);

CREATE INDEX idx_envio_guia ON Envio (num_guia);
CREATE INDEX idx_envio_logistica ON Envio (tipo_logistica);