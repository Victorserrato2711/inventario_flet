import flet as ft
from utils.mensajes import mostrar_mensaje_error
from views.login import login_view
from database import get_db

def logout_usuario():
    try:
        open("turno_actual.txt", "w").close()
        return {"ok": True, "mensaje": "Sesión cerrada"}
    except Exception as e:
        return {"ok": False, "mensaje": f"Error al cerrar sesión: {str(e)}"}
