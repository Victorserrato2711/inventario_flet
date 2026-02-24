import flet as ft
from services.usuario_service import cambiar_contraseña
from views.layout import app_layout


def cambiar_contraseña_view(page: ft.Page, db, refrescar_usuarios=None):
    usuario_field = ft.TextField(label="Usuario", width=300)
    nueva_field = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, width=300)
    confirmar_field = ft.TextField(label="Confirmación de Contraseña", password=True, can_reveal_password=True, width=300)

    def on_guardar(e):
        nueva = nueva_field.value.strip()
        confirmar = confirmar_field.value.strip()

        if nueva != confirmar:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()
            return

        if len(nueva) < 8:
            page.snack_bar = ft.SnackBar(ft.Text("La contraseña debe tener mínimo 8 caracteres"))
            page.snack_bar.open = True
            page.update()
            return

        if not any(c.isupper() for c in nueva):
            page.snack_bar = ft.SnackBar(ft.Text("La contraseña debe incluir al menos una mayúscula"))
            page.snack_bar.open = True
            page.update()
            return

        max_repe = 2
        count = 1
        for i in range(1, len(nueva)):
            if nueva[i] == nueva[i - 1]:
                count += 1
                if count > max_repe:
                    page.snack_bar = ft.SnackBar(ft.Text("La contraseña no puede repetir un mismo carácter más de 2 veces seguidas"))
                    page.snack_bar.open = True
                    page.update()
                    return
            else:
                count = 1

        resultado = cambiar_contraseña(db, usuario_field.value.strip(), nueva)
        page.snack_bar = ft.SnackBar(ft.Text(resultado["mensaje"]))
        page.snack_bar.open = True
        page.update()

        if resultado["ok"]:
            usuario_field.value = ""
            nueva_field.value = ""
            confirmar_field.value = ""
            page.update()

    def on_cancelar(e):
        usuario_field.value = ""
        nueva_field.value = ""
        confirmar_field.value = ""
        page.update()

    # ---- Pantalla Principal ----
    botones = ft.Row(
        controls=[
            ft.Button("Guardar", on_click=on_guardar, bgcolor="#28a745", color="white"),
            ft.Button("Cancelar", on_click=on_cancelar, bgcolor="#dc3545", color="white")
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    requisitos = ft.Column(
        [
            ft.Text("Requisitos de la contraseña:", size=18, color="yellow"),
            ft.Text("- Mínimo 8 caracteres", color="white"),
            ft.Text("- Al menos una letra mayúscula", color="white"),
            ft.Text("- Al menos un número", color="white"),
            ft.Text("- No repetir un mismo carácter más de 2 veces seguidas", color="white"),
        ],
        spacing=5,
        horizontal_alignment=ft.CrossAxisAlignment.START
    )

    formulario = ft.Column(
        [
            ft.Text("Cambio de Contraseña", size=30, weight=ft.FontWeight.BOLD, color="white"),
            usuario_field,
            nueva_field,
            confirmar_field,
            botones,
            ft.Container(height=20),
            requisitos
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    contenido_con_fondo = ft.Container(
        bgcolor="#282728",
        expand=True,
        content=formulario
    )

    return app_layout(
        page,
        contenido_con_fondo,
        selected_index=3
    )