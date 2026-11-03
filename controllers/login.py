import web

from config import context as ctx
from config.database import DatabaseError
from config.security import verify_password
from models import user as user_repo


class Login:
    def GET(self):
        if ctx.session.logged_in:
            raise web.seeother("/dashboard")
        return ctx.render.login(error=None)

    def POST(self):
        user_input = web.input(username="", password="")
        identifier = user_input.username.strip()
        password = user_input.password

        if not identifier or not password:
            return ctx.render.login(
                error="Escribe tu usuario o correo y tu contraseña."
            )

        try:
            user = user_repo.find_by_identifier(identifier)
        except DatabaseError as exc:
            print(f"Error de base de datos en login: {exc}")
            return ctx.render.login(
                error="No se pudo conectar con la base de datos. Intenta de nuevo."
            )

        if (
            user is None
            or not user["is_active"]
            or not verify_password(user["password_hash"], password)
        ):
            return ctx.render.login(error="Usuario o contraseña incorrectos.")

        ctx.session.logged_in = True
        ctx.session.user = user["username"]
        ctx.session.user_id = user["user_id"]
        ctx.session.full_name = (
            f"{user['first_name']} {user['last_name']}".strip()
        )
        ctx.session.role = user["role"]

        raise web.seeother("/dashboard")
