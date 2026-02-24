import flet as ft
from services.usuario_service import login_usuario
from utils.mensajes import mostrar_mensaje_error

def login_view(page: ft.Page, db):
    usuario_field = ft.TextField(label="Ingresa tu Usuario")
    contrasena_field = ft.TextField(label="Ingresa tu Contraseña", password=True)

    def on_ingresar(e):
        usuario = usuario_field.value.strip()
        contrasena = contrasena_field.value.strip()

        if not usuario or not contrasena:
            mostrar_mensaje_error(page, "Usuario y contraseña requeridos")
            return

        resultado = login_usuario(db, usuario, contrasena)

        if not resultado["ok"]:
            mostrar_mensaje_error(page, resultado["mensaje"])
            return

        if resultado.get("requiere_cambio", False):
            page.go(f"/cambio_contraseña_login?usuario={usuario}")
        else:
            # Guardamos los datos del usuario en atributos de page
            page.usuario_id = resultado["usuario"]["id"]
            page.usuario_nombre = resultado["usuario"]["nombre"]

            page.go("/home")

    boton_login = ft.Button(
        "Ingresar",
        icon=ft.Icons.LOGIN,
        bgcolor="#1976D2",
        color="white",
        on_click=on_ingresar
    )

    return ft.Container(
        expand=True,
        alignment=ft.alignment.Alignment(0.0, 0.0),
        content=ft.Column(
            [
                ft.Text("Inicio Sesión", size=20, weight="bold", color="red"),
                usuario_field,
                contrasena_field,
                boton_login
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )