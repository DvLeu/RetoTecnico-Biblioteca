# Sistema de Biblioteca

Solución desarrollada con Django para la gestión de autores, usuarios, libros y préstamos. Incluye una API REST documentada y soporte para contenedores.

## Tecnologías utilizadas

* **Core:** Python 3.11, Django 5.2
* **API:** Django REST Framework, Swagger (OpenAPI)
* **DB:** PostgreSQL 15
* **Infraestructura:** Docker & Docker Compose

## Instalación y despliegue

1. **Clonar el repositorio:**
   **Bash**

   ```
   git clone https://github.com/DvLeu/RetoTecnico-Biblioteca.git
   cd RetoTecnico-Biblioteca
   ```
2. **Configurar variables de entorno:**
   **Bash**

   ```
   cp .env.example .env
   ```
3. **Levantar con Docker:**
   **Bash**

   ```
   docker compose up --build
   ```

*Al iniciar, el contenedor ejecutará automáticamente las migraciones, la creación de un usuario de prueba y la carga de datos iniciales.*

## Acceso al sistema

**Credenciales de prueba:**

* **Usuario:** `appix`
* **Contraseña:** `retoappix`

**URLs locales:**

* **Web App:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **Admin Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* **Documentación Swagger:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
* **API Root:** [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

## Módulos y API

El sistema gestiona cuatro entidades principales:  **Autores, Usuarios, Libros y Préstamos** .

### API Endpoints

* `/api/autores/`
* `/api/usuarios/`
* `/api/libros/`
* `/api/prestamos/`
* *Nota: Se requiere autenticación para interactuar con los endpoints.*

### Gestión Web

El CRUD de préstamos es accesible desde la ruta `/prestamos/`, permitiendo:

* Visualización del historial.
* Registro de nuevos préstamos.
* Edición y eliminación de registros.

## Detalles técnicos

* **Identificadores:** Se utilizan `UUID` en lugar de IDs incrementales para los registros.
* **Seguridad de Datos:** Las relaciones entre modelos utilizan `on_delete=models.PROTECT` para evitar borrados accidentales de registros vinculados.
* **Modelos:** Se diferencia el usuario interno de Django (auth/admin) del modelo `Usuario` específico de la biblioteca.
* **Portabilidad:** Configuración lista para entornos de desarrollo mediante Docker.
