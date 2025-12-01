# logistica-prueba-tecnica

 Logística API: Prueba Técnica (FastAPI + PostgreSQL + Docker)Este proyecto implementa una API RESTful robusta para la gestión de envíos bajo dos modelos logísticos principales: Terrestre y Marítimo.La solución utiliza FastAPI para el backend, PostgreSQL como base de datos y Docker Compose para orquestar todo el entorno.

 Requisitos Previos 
 Necesitas tener instalados los siguientes programas:
 Docker y Docker Compose (Esencial para la infraestructura).
 Git.Node.js / npm (Para ejecutar el Frontend de React/Vite). 
 
 1. Inicio Rápido (Levantar el Entorno)Sigue estos pasos para levantar la infraestructura y ejecutar la aplicación.
    1.1. Clonar e Iniciar la InfraestructuraAsegúrate de estar en la carpeta raíz del proyecto y ejecuta:Bash# 1. Clonar el repositorio (si aplica)
    # git clone <https://github.com/MauricioChavarria/logistica-prueba-tecnica.git>
    # cd <logistica-prueba-tecnica>

    Construir y levantar la API y la DB en segundo plano
    docker compose up --build -d

    1.2. Inicializar la Base de DatosUna vez que el contenedor db esté activo, ejecuta el script de esquema para crear las tablas:
    Inicializa el esquema usando el archivo database/schema.sql
        docker exec -i logistica_db psql -U postgres -d logistica_db < database/schema.sql

    1.3. Ejecutar el Frontend (Interfaz de Usuario)El Frontend de React/Vite te permite interactuar fácilmente con la API.
    cd frontend
    npm install
    npm run dev

2. Endpoints de la API y SeguridadLa API de FastAPI está disponible en http://localhost:8000.
    AutenticaciónTodos los endpoints están protegidos. Debes incluir el siguiente header en cada solicitud (el Frontend ya lo implementa)
    
    Header: Authorization
    Valor: Bearer 



3. Pruebas Unitarias (Pytest)Las pruebas unitarias y de integración son cruciales y están implementadas para verificar la lógica de descuentos, los formatos de validación y la seguridad (HTTP 401).
Para ejecutar las pruebas:
    cd backend
    pytest

5. Detener el Entorno
    docker compose down