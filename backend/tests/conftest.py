import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db
import app.database.models as models 

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    """Fixture para crear una sesión de base de datos de prueba."""
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 
    
    db = TestingSessionLocal()
    
    db.add(models.Cliente(nombre="Test Cliente", contacto="999", email="test@example.com"))
    db.add(models.TipoProducto(nombre="Fragil"))
    db.add(models.Bodega(nombre="Bodega Central", direccion="Calle Test"))
    db.add(models.Puerto(nombre="Puerto Marítimo", ubicacion="Costo Test"))
    db.commit()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    """Fixture para el cliente de prueba de FastAPI."""
    
    def override_get_db():
        try:
            yield session
        finally:
            session.close() 

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()