# FastAPI Tareas API

API de gestión de tareas con autenticación JWT y soporte multiusuario.

## 🚀 Funcionalidades

- Registro de usuarios
- Login con JWT
- CRUD de tareas
- Rutas protegidas
- Contraseñas encriptadas (bcrypt)

## 🛠️ Tecnologías

- FastAPI
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)

## 🔐 Uso

1. Registrar usuario:
POST /registro

2. Login:
POST /login

3. Usar token:
Authorization: Bearer <token>

4. Obtener tareas:
GET /tareas
