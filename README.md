# virtual_physics_laboratory

Laboratorio virtual de física para la UTP: simulaciones, grupos, ranking y logros.

## Requisitos

- Python 3.13
- PostgreSQL en Supabase

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edita .env con las credenciales de tu proyecto de Supabase
```

## Base de datos

El esquema vive en Supabase. Las tablas esperadas son:

- `users`
- `degree_programs`
- `groups`
- `group_students`
- `lab_experiments`
- `group_lab_assignments`
- `lab_attempts`

Las vistas de ranking (`view_leaderboard`, `view_group_progress`) todavía no
están creadas en la base. Ejecuta `sql/views.sql` en el SQL Editor de Supabase.

### Contraseñas

Los usuarios de prueba se insertaron con la contraseña en texto plano dentro
de `password_hash`. El login acepta ambos formatos para no romper nada, pero
conviene migrarlos:

```bash
python -m scripts.hash_passwords
```

Después de eso las contraseñas quedan guardadas como
`pbkdf2_sha256$600000$...`.

## Ejecutar

```bash
python app.py          # http://localhost:8080
python app.py 8099     # otro puerto
```

Para producción:

```bash
WEB_DEBUG=0 gunicorn app:application
```

## Estructura

```
app.py                  rutas, aplicación y arranque
config/
  context.py            sesión y renderizador compartidos
  database.py           conexión y consultas a Supabase
  security.py           hash/verificación de contraseñas
controllers/            controladores de web.py
models/                 consultas por entidad (users, groups)
views/                  plantillas de web.py
scripts/                tareas puntuales (migrar contraseñas)
sql/                    scripts SQL auxiliares
```

## Flujo de autenticación

1. `POST /login` recibe usuario (o correo) y contraseña.
2. Se busca el usuario en `users` por `username` o `email`.
3. Se verifica `is_active` y `password_hash`.
4. Se guardan `user_id`, `user`, `full_name` y `role` en la sesión.
5. `/dashboard` muestra los grupos según el rol (`STUDENT` o `PROFESSOR`).
6. `/logout` ejecuta `session.kill()` y expira la cookie.
