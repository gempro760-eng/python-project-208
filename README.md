# Hexlet Task Manager

[![Maintainability](https://api.codeclimate.com/v1/badges/your-badge-token/maintainability)](https://codeclimate.com/github/gempro760-eng/python-project-208)
[![Test Coverage](https://api.codeclimate.com/v1/badges/your-badge-token/test_coverage)](https://codeclimate.com/github/gempro760-eng/python-project-208)

Task Manager es un sistema web de gestión de tareas desarrollado con **Django** y **Bootstrap 5**. Permite organizar proyectos, asignar tareas a miembros del equipo, dar seguimiento a estados y administrar usuarios mediante control de acceso y autenticación.

## 🚀 Despliegue en producción

La aplicación se encuentra desplegada y funcionando en la nube:

* **Enlace activo en Render:** [https://python-project-208-pj9t.onrender.com](https://python-project-208-pj9t.onrender.com)

---

## 🛠️ Tecnologías utilizadas

* **Lenguaje:** Python >= 3.12
* **Framework Backend:** Django 6.x
* **Frontend:** Bootstrap 5 (`django-bootstrap5`)
* **Gestor de paquetes y entorno:** `uv`
* **Linter y formateador:** `ruff`
* **Base de datos:** SQLite (local) / PostgreSQL (`dj-database-url` en producción)
* **Servidor WSGI:** Gunicorn

---

## 📋 Funcionalidades implementadas

* **Autenticación y usuarios:** Registro, inicio de sesión, cierre de sesión, listado y edición/eliminación protegida por propietario.
* **CRUD de Estados:** Creación, edición, listado y eliminación segura de estados para tareas.
* **CRUD de Tareas:** Creación, edición, detalle y eliminación de tareas restringida al autor.
* **Control de accesos:** Restricción de operaciones críticas a usuarios autenticados.
* **Mensajes flash:** Retroalimentación visual interactiva en cada operación.

---

## 💻 Instalación y ejecución local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/gempro760-eng/python-project-208.git](https://github.com/gempro760-eng/python-project-208.git)
cd python-project-208
