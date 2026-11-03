import os
import web
from config import context

# debug=True muestra errores detallados y no cachea plantillas (útil en local).
# En producción exporta WEB_DEBUG=0.
web.config.debug = os.environ.get("WEB_DEBUG", "1") == "1"

# Definición de rutas
urls = (
    "/", "controllers.index.Index",
    "/login", "controllers.login.Login",
    "/logout", "controllers.logout.Logout",
    "/dashboard", "controllers.dashboard.Dashboard",
)

# autoreload=False evita que web.py vuelva a importar app.py (y cree una
# segunda aplicación sin sesión) al arrancar con debug activado.
app = web.application(urls, globals(), autoreload=False)

# Sesión + renderizador compartidos con los controladores.
context.init(app)

# Punto de entrada para gunicorn/uWSGI: gunicorn app:application
application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
