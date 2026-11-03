import web

from config import context as ctx
from config.database import DatabaseError
from models import group as group_repo

ROLE_LABELS = {
    "ADMINISTRATOR": "Administrador",
    "PROFESSOR": "Profesor",
    "STUDENT": "Estudiante",
}


class Dashboard:
    def GET(self):
        # Ruta protegida: sin sesión no se entra.
        if not ctx.session.logged_in:
            raise web.seeother("/login")

        role = ctx.session.role
        groups = []
        error = None

        try:
            if role == "STUDENT":
                groups = group_repo.list_for_student(ctx.session.user_id)
            elif role == "PROFESSOR":
                groups = group_repo.list_for_professor(ctx.session.user_id)
        except DatabaseError as exc:
            print(f"Error de base de datos en dashboard: {exc}")
            error = "No se pudieron cargar tus grupos en este momento."

        return ctx.render.dashboard(
            full_name=ctx.session.full_name,
            username=ctx.session.user,
            role=ROLE_LABELS.get(role, role),
            groups=groups,
            error=error,
        )
