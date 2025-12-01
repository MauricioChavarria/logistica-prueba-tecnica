from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.crud.crud_envio import calcular_descuento

# PRUEBAS DE LOGICA

def test_calcular_descuento_terrestre_con_descuento():
    """Debe aplicar el 5% de descuento para Terrestre si cantidad > 10."""
    precio_base = 1000.00
    cantidad = 15
    precio_final, descuento = calcular_descuento(precio_base, cantidad, "Terrestre")
    
    # 5% de 1000 es 50.00
    assert descuento == 50.00
    assert precio_final == 950.00

def test_calcular_descuento_maritimo_con_descuento():
    """Debe aplicar el 3% de descuento para Marítimo si cantidad > 10."""
    precio_base = 1000.00
    cantidad = 15
    precio_final, descuento = calcular_descuento(precio_base, cantidad, "Maritimo")
    
    # 3% de 1000 es 30.00
    assert descuento == 30.00
    assert precio_final == 970.00

def test_calcular_descuento_sin_descuento():
    """No debe aplicar descuento si cantidad <= 10."""
    precio_base = 1000.00
    cantidad = 10
    precio_final, descuento = calcular_descuento(precio_base, cantidad, "Terrestre")
    
    assert descuento == 0.00
    assert precio_final == 1000.00

# PRUEBAS DE INTEGRACION

# Datos de prueba comunes
today = date.today().isoformat()
tomorrow = (date.today() + timedelta(days=1)).isoformat()

AUTH_HEADER = {"Authorization": "Bearer TEST_BEARER_TOKEN_2025"}
BASE_URL = "/v1"

def test_create_envio_terrestre_success(client: TestClient):
    """Prueba de registro exitoso de envío terrestre."""
    data = {
        "cliente_id": 1,
        "tipo_producto_id": 1,
        "cantidad": 12, # Cantidad > 10 para probar descuento
        "fecha_registro": today,
        "fecha_entrega": tomorrow,
        "precio_envio": 500.00,
        "placa_vehiculo": "ABC123", # Formato AAA999
        "bodega_id": 1
    }
    
    response = client.post(f"{BASE_URL}/terrestre/envios", json=data, headers=AUTH_HEADER)
    
    assert response.status_code == 201
    json_data = response.json()
    
    # 5% de 500.00 es 25.00
    assert json_data["precio_base"] == 500.00
    assert json_data["descuento_aplicado"] == 25.00
    assert json_data["precio_final"] == 475.00
    assert json_data["tipo_logistica"] == "Terrestre"
    assert json_data["num_guia"] is not None
    assert json_data["placa_vehiculo"] == "ABC123"
    assert json_data["num_flota"] is None # Marítimo debe ser NULL

def test_create_envio_terrestre_invalid_placa(client: TestClient):
    """Prueba de formato de placa de vehículo inválida."""
    data = {
        "cliente_id": 1, "tipo_producto_id": 1, "cantidad": 5, 
        "fecha_registro": today, "fecha_entrega": tomorrow, "precio_envio": 100.00,
        "placa_vehiculo": "123ABC", # Formato INCORRECTO
        "bodega_id": 1
    }
    
    response = client.post(f"{BASE_URL}/terrestre/envios", json=data, headers=AUTH_HEADER)
    
    # Debe fallar la validación de Pydantic
    assert response.status_code == 422 


def test_create_envio_maritimo_success(client: TestClient):
    """Prueba de registro exitoso de envío marítimo."""
    data = {
        "cliente_id": 1,
        "tipo_producto_id": 1,
        "cantidad": 20, # Cantidad > 10 para probar descuento
        "fecha_registro": today,
        "fecha_entrega": tomorrow,
        "precio_envio": 2000.00,
        "num_flota": "XYZ7890A", # Formato AAA9999A
        "puerto_id": 1
    }
    
    response = client.post(f"{BASE_URL}/maritimo/envios", json=data, headers=AUTH_HEADER)
    
    assert response.status_code == 201
    json_data = response.json()

    # 3% de 2000.00 es 60.00
    assert json_data["precio_base"] == 2000.00
    assert json_data["descuento_aplicado"] == 60.00
    assert json_data["precio_final"] == 1940.00
    assert json_data["tipo_logistica"] == "Maritimo"
    assert json_data["placa_vehiculo"] is None # Terrestre debe ser NULL

def test_get_envios_by_filter_num_guia(client: TestClient):
    """Prueba de filtrado por número de guía en la consulta marítima."""
    # 1. Crear un envío específico
    data = {
        "cliente_id": 1, "tipo_producto_id": 1, "cantidad": 5, 
        "fecha_registro": today, "fecha_entrega": tomorrow, "precio_envio": 100.00,
        "num_flota": "FRO9999T", "puerto_id": 1
    }
    create_response = client.post(f"{BASE_URL}/maritimo/envios", json=data, headers=AUTH_HEADER)
    num_guia = create_response.json()["num_guia"] # Obtenemos la guía generada

    # 2. Consultar con el filtro
    query_response = client.get(
        f"{BASE_URL}/maritimo/envios", 
        params={"num_guia": num_guia},
        headers=AUTH_HEADER
    )
    
    assert query_response.status_code == 200
    assert len(query_response.json()) == 1
    assert query_response.json()[0]["num_guia"] == num_guia

