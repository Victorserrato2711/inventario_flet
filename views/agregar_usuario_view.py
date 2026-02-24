import flet as ft
from services.usuario_service import crear_usuario
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error
from views.layout import app_layout

def agregar_usuario_view(page: ft.Page, db, refrescar_usuarios):
    # --- Campos del formulario ---
    usuario_field = ft.TextField(label="Usuario")
    nombre_field = ft.TextField(label="Nombre")
    correo_field = ft.TextField(label="Correo")
    puesto_field = ft.TextField(label="Puesto")

    def on_guardar(ev):
        resultado = crear_usuario(
            db,
            usuario=usuario_field.value.strip(),
            nombre=nombre_field.value.strip(),
            correo=correo_field.value.strip(),
            puesto=puesto_field.value.strip()
        )

        if resultado["ok"]:
            mostrar_mensaje(page,resultado["mensaje"],color="#28a745")
            refrescar_usuarios()
            from views.usuarios_view import usuario_view
            page.views.clear()
            page.views.append(usuario_view(page, db, refrescar_usuarios))
            page.update()
        else:
            mostrar_mensaje_error(page,resultado["mensaje"])

    # --- contenido principal ---
    contenido = ft.Column(
        [
            ft.Text("Agregar Usuario", size=25, color="#FFFFFF"),
            usuario_field,
            nombre_field,
            correo_field,
            puesto_field,
            ft.Row(
                controls=[
                    ft.Button(
                        "Guardar",
                        on_click=on_guardar,
                        bgcolor="#008000",
                        color="#FFFFFF"
                    ),
                    ft.Button(
                        "Volver",
                        on_click=lambda e: (
                            page.views.clear(),
                            page.views.append(__import__("views.usuarios_view").usuarios_view.usuario_view(page, db, refrescar_usuarios)),
                            page.update()
                        ),
                        bgcolor="#6C757D",
                        color="#FFFFFF"
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    return app_layout(
        page,
        contenido_con_fondo,
        selected_index=2
    )