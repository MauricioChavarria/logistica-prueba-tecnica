# Logística API: Prueba Técnica (FastAPI + PostgreSQL + Docker + React)

Este proyecto implementa una solución completa para la gestión de envíos de productos bajo dos modelos logísticos principales: **Terrestre** y **Marítimo**.

La solución integra un *backend* robusto con **FastAPI** y **PostgreSQL**, orquestado con **Docker Compose**, y un *frontend* interactivo con **React (Vite)**.

##  Requisitos Previos

Necesitas tener instalados los siguientes programas:

* **Docker** y **Docker Compose** (Esencial para la infraestructura).
* **Git**.
* **Node.js / npm** (Para ejecutar el Frontend de React).

---

##  1. Inicio Rápido (Levantar el Entorno)
Sigue estos pasos para levantar la infraestructura completa, incluyendo la base de datos y la interfaz de usuario.
1.1. Iniciar la Infraestructura
Asegúrate de estar en la carpeta raíz del proyecto y ejecuta:
* docker compose up --build -d

1.2. Inicializar la Base de Datos
Una vez que el contenedor db esté activo, ejecuta el script de esquema para crear las tablas y las referencias:
* docker exec -i logistica_db psql -U postgres -d logistica_db < database/schema.sql

1.3. Ejecutar el Frontend
El Frontend se ejecuta en modo de desarrollo local:
* cd frontend
* npm install
* npm run dev
  
La interfaz de usuario estará disponible en tu navegador en http://localhost:5173/.

# 2. Endpoints de la API y Seguridad
La API de FastAPI está disponible en http://localhost:8000. Autenticación (Seguridad)Todos los endpoints están protegidos. Debes incluir el siguiente header en cada solicitud (el Frontend ya lo implementa):
* Header: Authorization
* Valor: Bearer

# 3. Lógica de Negocio Implementada
La aplicación valida los datos y aplica descuentos según las siguientes reglas:
* Requisito Logística TerrestreLogística Marítima
* Descuento 5% si la cantidad de producto es mayor a 10. 3% si la cantidad de producto es mayor a 10.
* Validación Placa Formato AAA999 (3 letras, 3 números). N/A
* Validación Flota N/A Formato AAA9999A (3 letras, 4 números, 1 letra).
* ID de RastreoGeneración de num_guia alfanumérico único de 10 dígitos.

# 4. Pruebas Unitarias (Pytest)
Las pruebas unitarias y de integración son cruciales y están implementadas en la carpeta backend/tests/ para verificar la lógica de negocio, las validaciones de formato y la seguridad (HTTP 401).
Para ejecutar las pruebas:

* cd backend
* pytest

# 5. Detener el EntornoPara detener y limpiar todos los contenedores al finalizar:
docker compose down

# 6 Diagrama E-R
* https://dbdiagram.io/d/692d6d26d6676488ba0da17f
