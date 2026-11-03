import web

from config import context as ctx


class Index:
    def GET(self):
        # Si ya inició sesión, directo al panel; si no, a la portada.
        if ctx.session.logged_in:
            raise web.seeother("/dashboard")
        return ctx.render.index()
