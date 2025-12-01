from fastapi.testclient import TestClient
from datetime import date, timedelta
import json

# Datos de prueba mínimos para POST
today = date.today().isoformat()
tomorrow = (date.today() + timedelta(days=1)).isoformat()
BASE_URL = "/v1"

terrestre_data = {
    "cliente_id": 1, "tipo_producto_id": 1, "cantidad": 5, 
    "fecha_registro": today, "fecha_entrega": tomorrow, "precio_envio": 100.00,
    "placa_vehiculo": "XYZ777", "bodega_id": 1
}

maritimo_data = {
    "cliente_id": 1, "tipo_producto_id": 1, "cantidad": 5, 
    "fecha_registro": today, "fecha_entrega": tomorrow, "precio_envio": 100.00,
    "num_flota": "FRO1111A", "puerto_id": 1
}

def test_unauthorized_post_terrestre(client: TestClient):
    """POST Terrestre debe fallar sin token."""
    response = client.post(f"{BASE_URL}/terrestre/envios", json=terrestre_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_unauthorized_post_maritimo(client: TestClient):
    """POST Marítimo debe fallar sin token."""
    response = client.post(f"{BASE_URL}/maritimo/envios", json=maritimo_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_unauthorized_get_terrestre(client: TestClient):
    """GET Terrestre debe fallar sin token."""
    response = client.get(f"{BASE_URL}/terrestre/envios")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_unauthorized_get_maritimo(client: TestClient):
    """GET Marítimo debe fallar sin token."""
    response = client.get(f"{BASE_URL}/maritimo/envios")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_unauthorized_with_wrong_token(client: TestClient):
    """Debe fallar con un token JWT inválido (diferente al TEST_BEARER_TOKEN_2025)."""
    wrong_header = {"Authorization": "Bearer WRONG_TOKEN_XYZ"}
    response = client.get(f"{BASE_URL}/terrestre/envios", headers=wrong_header)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"