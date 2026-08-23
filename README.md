# Hexlet Task Manager

[![hexlet-check](https://github.com/gempro760-eng/python-project-208/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/gempro760-eng/python-project-208/actions/workflows/hexlet-check.yml)

Aplicacion web para gestionar tareas pendientes con Django. Permite registrar usuarios, autenticar sesiones, administrar estados y etiquetas, asignar ejecutores y filtrar tareas.

## Produccion

La aplicacion esta disponible en Render:

https://python-project-208-pj9t.onrender.com

## Requisitos

- Python 3.12 o superior
- uv
- Docker y Docker Compose para ejecutar el entorno de CI localmente

## Instalacion

```bash
git clone https://github.com/gempro760-eng/python-project-208.git
cd python-project-208
uv sync
uv run python manage.py migrate
```

Para crear un administrador:

```bash
uv run python manage.py createsuperuser
```

## Ejecucion local

```bash
uv run python manage.py runserver
```

La aplicacion queda disponible en `http://127.0.0.1:8000/`.

## Variables de entorno

En produccion se recomienda configurar:

```text
DJANGO_SECRET_KEY=clave-secreta
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=dominio.onrender.com,webserver
DATABASE_URL=postgres://usuario:contrasena@host:5432/base
SENTRY_DSN=dsn-del-servicio
ENVIRONMENT=production
```

La aplicacion usa SQLite por defecto en desarrollo y PostgreSQL cuando se define `DATABASE_URL`.

## Funcionalidades

- Registro, login y logout mediante la autenticacion de Django.
- Edicion y eliminacion del propio perfil.
- CRUD protegido de estados y etiquetas.
- CRUD de tareas con autor, ejecutor, estado y multiples etiquetas.
- Proteccion contra la eliminacion de usuarios, estados o etiquetas asociados.
- Eliminacion de tareas limitada a su autor.
- Filtros por `status`, `executor`, `label` y `self_tasks`.

## Calidad

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run ruff check .
uv run coverage run -m pytest
uv run coverage report --fail-under=80
```

El proyecto tambien incluye `build.sh`, `Makefile`, Docker Compose y migraciones para el despliegue.

## Despliegue en Render

Configura el servicio con:

- Build command: `make build`
- Start command: `make render-start`

Define las variables de entorno de produccion antes de desplegar. El script de build instala dependencias, recopila estaticos y ejecuta migraciones.
