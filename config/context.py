"""Objetos compartidos por la aplicación: plantillas y sesión.

Los controladores no deben crear su propio `render` ni su propia `Session`.
Si cada módulo lo hiciera, web.py registraría varias sesiones sobre la misma
aplicación y las cookies se pisarían entre sí.
"""

import os

import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, "views")
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")

# `render` se crea en init() porque la plantilla base necesita la sesión.
render = None
session = None


def init(app):
    """Crea (una sola vez) la sesión y el renderizador de plantillas."""
    global render, session

    # web.config es global al proceso. Si el módulo se importa dos veces,
    # reutilizamos la sesión ya creada en lugar de registrar otra.
    if web.config.get("_session") is None:
        session = web.session.Session(
            app,
            web.session.DiskStore(SESSIONS_DIR),
            initializer={
                "logged_in": False,
                "user": None,
                "user_id": None,
                "full_name": None,
                "role": None,
            },
        )
        web.config._session = session
    else:
        session = web.config._session

    render = web.template.render(VIEWS_DIR, base="layout")

    return session
