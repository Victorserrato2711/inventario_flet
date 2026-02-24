import flet as ft
import re
from services.usuario_service import cambiar_contraseña
from models import Usuario
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error

def cambio_contraseña_login_view(page: ft.Page, usuario: str, db):
    nueva_field = ft.TextField(label="Nueva Contraseña", password=True)
    confirmar_field = ft.TextField(label="Confirma la contraseña", password=True)

    # --- Validación de requisitos ---
    def validar_contrasena(password: str):
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres"
        if not re.search(r"[A-Z]", password):
            return "Debe contener al menos una letra mayúscula"
        if not re.search(r"[a-z]", password):
            return "Debe contener al menos una letra minúscula"
        if not re.search(r"[0-9]", password):
            return "Debe contener al menos un número"
        if not re.search(r"[^A-Za-z0-9]", password):
            return "Debe contener al menos un carácter especial"
        return None

    def on_guardar(e):

        if not nueva_field.value.strip() or not confirmar_field.value.strip():
            mostrar_mensaje_error(page, "Debe llenar todos los campos")
            return

        if nueva_field.value.strip() != confirmar_field.value.strip():
            mostrar_mensaje_error(page, "Las contraseñas no coinciden")
            return

        error = validar_contrasena(nueva_field.value.strip())
        if error:
            mostrar_mensaje_error(page, error)
            return

        resultado = cambiar_contraseña(db, usuario, nueva_field.value.strip())
        if resultado["ok"]:
            usuario_obj = db.query(Usuario).filter(Usuario.usuario == usuario).first()
            usuario_obj.requiere_cambio = False  # Desactivar flag
            db.commit()

            mostrar_mensaje(page, "Contraseña actualizada con éxito", color="#28a745")
            page.go("/home")
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    def on_cancelar(e):
        nueva_field.value = ""
        confirmar_field.value = ""
        page.update()

    boton_guardar = ft.Button("Guardar", on_click=on_guardar, bgcolor="#008000", color="#FFFFFF")
    boton_cancelar = ft.Button("Cancelar", on_click=on_cancelar, bgcolor="#6C757D", color="#FFFFFF")

    # --- contenido principal ---
    contenido = ft.Column(
        [
            ft.Text("Debe cambiar su contraseña antes de continuar", size=18, weight="bold", color="#FFFFFF"),
            nueva_field,
            confirmar_field,
            ft.Container(
                content=ft.Column([
                    ft.Text("La nueva contraseña debe cumplir con:", color="#FFFFFF"),
                    ft.Text("- Mínimo 8 caracteres", color="#FFFFFF"),
                    ft.Text("- Al menos una letra mayúscula", color="#FFFFFF"),
                    ft.Text("- Al menos una letra minúscula", color="#FFFFFF"),
                    ft.Text("- Al menos un número", color="#FFFFFF"),
                    ft.Text("- Al menos un carácter especial", color="#FFFFFF"),
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY),
                border_radius=5
            ),
            ft.Row([boton_guardar, boton_cancelar], alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    return ft.Container(
        bgcolor="#282728",
        expand=True,
        alignment=ft.alignment.Alignment(0.5, 0.5),
        content=contenido
    )