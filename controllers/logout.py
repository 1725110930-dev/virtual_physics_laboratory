import web

from config import context as ctx


class Logout:
    def GET(self):
        # Borra la sesión del almacenamiento y expira la cookie.
        ctx.session.kill()
        raise web.seeother("/login")
