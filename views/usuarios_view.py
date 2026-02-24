import flet as ft
from database import Session
import services.usuario_service
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error
from views.layout import app_layout
from views.agregar_usuario_view import agregar_usuario_view


def usuario_view(page: ft.Page, db=None, refrescar_home=None):
    page.title = "Gestión de Usuarios"
    db = db or Session()

    txt_buscar = ft.TextField(label="Buscar por Nombre", width=300, on_submit=lambda e: mostrar_usuarios())
    contenido = ft.Column(expand=True)

    # ---- Habilitar Usuario -----

    def ir_habilitar_usuario(usuario_id, nombre_usuario):
        def ejecutar_habilitacion(uid):
            resultado = services.usuario_service.habilitar_usuario(db, uid)
            if resultado["ok"]:
                mostrar_mensaje(page, f"El Usuario {nombre_usuario} ha sido habilitado", color="#28a745")
                if refrescar_home:
                    refrescar_home()
            else:
                mostrar_mensaje_error(page, "Error: Usuario no encontrado")

            # Navegación explícita: volver a la lista de usuarios
            page.views.clear()
            page.views.append(usuario_view(page, db, refrescar_home))
            page.update()

        confirmacion = ft.Container(
            bgcolor=ft.Colors.BLACK,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"¿Seguro que deseas habilitar al usuario '{nombre_usuario}'?",
                        color="WHITE"
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                "Sí, Habilitar",
                                bgcolor="#28a745",
                                color="WHITE",
                                on_click=lambda e: ejecutar_habilitacion(usuario_id)
                            ),
                            ft.Button(
                                "Cancelar",
                                bgcolor="#6C757D",
                                color="WHITE",
                                on_click=lambda e: page.controls.remove(confirmacion) or page.update()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.controls.append(confirmacion)
        page.update()

    # --- Deshabilitar usuario ---
    def ir_deshabilitar_usuario(usuario_id, nombre_usuario):
        def ejecutar_deshabilitacion(uid):
            resultado = services.usuario_service.deshabilitar_usuario(db, uid)
            if resultado["ok"]:
                mostrar_mensaje(page, f"Usuario {nombre_usuario} deshabilitado con éxito", color="#28a745")
                if refrescar_home:
                    refrescar_home()
            else:
                mostrar_mensaje_error(page, "Error: Usuario no encontrado")

            page.views.clear()
            page.views.append(usuario_view(page, db, refrescar_home))
            page.update()

        def quitar_confirmacion(e=None):
            if confirmacion in page.controls:
                page.controls.remove(confirmacion)
                page.update()

        confirmacion = ft.Container(
            bgcolor=ft.Colors.BLACK,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"¿Seguro que deseas deshabilitar al usuario '{nombre_usuario}'?",
                        color="WHITE"
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                "Sí, Deshabilitar",
                                bgcolor="#DC3545",
                                color="WHITE",
                                on_click=lambda e: ejecutar_deshabilitacion(usuario_id)
                            ),
                            ft.Button(
                                "Cancelar",
                                bgcolor="#6C757D",
                                color="WHITE",
                                on_click=quitar_confirmacion
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.controls.append(confirmacion)
        page.update()

    # --- Editar usuario ---
    def ir_editar_usuario(usuario_id):
        usuarios = services.usuario_service.listar_usuarios(db)["usuarios"]
        usuario = next((u for u in usuarios if u["id"] == usuario_id), None)

        if not usuario:
            mostrar_mensaje_error(page, "Usuario no encontrado")
            return

        usuario_field = ft.TextField(label="Usuario", value=usuario["usuario"], disabled=True)
        nombre = ft.TextField(label="Nombre", value=usuario["nombre"])
        correo = ft.TextField(label="Correo", value=usuario["correo"])
        puesto = ft.TextField(label="Puesto", value=usuario["puesto"])

        def guardar_cambios(e):
            resultado = services.usuario_service.editar_usuario(
                db,
                usuario_id,
                nombre=nombre.value,
                correo=correo.value,
                puesto=puesto.value
            )
            if resultado["ok"]:
                mostrar_mensaje(page, f"Usuario {nombre.value} actualizado con éxito", color="#28a745")
                if refrescar_home:
                    refrescar_home()
            else:
                mostrar_mensaje_error(page, "Error al actualizar usuario")

            page.views.clear()
            page.views.append(usuario_view(page, db, refrescar_home))
            page.update()

        editar_view = ft.View(
            route=f"/editar_usuario/{usuario_id}",
            controls=[
                ft.Column(
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Editar Usuario", size=30, weight="bold", color="WHITE"),
                        usuario_field,
                        nombre,
                        correo,
                        puesto,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Button("Guardar", bgcolor="#008000", color="WHITE", on_click=guardar_cambios),
                                ft.Button("Cancelar", bgcolor="#6C757D", color="WHITE",
                                          on_click=lambda e: page.views.clear() or page.views.append(
                                              usuario_view(page, db, refrescar_home)) or page.update())
                            ]
                        )
                    ],
                    expand=True
                )
            ]
        )

        page.views.append(editar_view)
        page.update()

    # --- Mostrar usuarios ---
    def mostrar_usuarios(e=None):
        resultado = services.usuario_service.listar_usuarios(db)
        usuarios = resultado["usuarios"]

        filtro = txt_buscar.value.lower()
        if filtro:
            usuarios = [u for u in usuarios if filtro in u["nombre"].lower()]

        contenido.controls.clear()
        tabla = ft.DataTable(
            bgcolor="#1E1E1E",
            heading_row_color=ft.Colors.BLUE_GREY_900,
            border=ft.border.all(1, ft.Colors.GREY),
            columns=[
                ft.DataColumn(ft.Text("Usuario", weight="bold", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Nombre", weight="bold", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Puesto", weight="bold", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Activo", weight="bold", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Correo", weight="bold", color=ft.Colors.WHITE)),
                ft.DataColumn(ft.Text("Acciones", weight="bold", color=ft.Colors.WHITE))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(u["usuario"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(u["nombre"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(u["puesto"], color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text("Sí" if u["activo"] else "No", color=ft.Colors.WHITE)),
                        ft.DataCell(ft.Text(u["correo"], color=ft.Colors.WHITE)),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                        icon_color=ft.Colors.AMBER,
                                        on_click=lambda e, uid=u["id"]: ir_editar_usuario(uid)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE if u["activo"] else ft.Icons.RESTORE,
                                        tooltip="Deshabilitar" if u["activo"] else "Habilitar",
                                        icon_color=ft.Colors.RED if u["activo"] else ft.Colors.GREEN,
                                        on_click=lambda e, uid=u["id"], nombre=u["nombre"]:
                                        ir_deshabilitar_usuario(uid, nombre) if u["activo"] else ir_habilitar_usuario(
                                            uid, nombre)
                                    )
                                ]
                            )
                        )
                    ]
                )
                for u in usuarios
            ]
        )

        contenido.controls.append(
            ft.Container(
                content=tabla,
                alignment=ft.alignment.Alignment(0, 0),
                expand=True
            )
        )
        page.update()

    btn_agregar = ft.Button(
        "Agregar Usuario",
        bgcolor="#008000",
        color="#FFFFFF",
        on_click=lambda e: mostrar_formulario_agregar()
    )

    def mostrar_formulario_agregar():
        page.views.clear()
        page.views.append(
            agregar_usuario_view(page, db, mostrar_usuarios)
        )
        page.update()

    layout = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Gestión de Usuarios", size=40, color="#FFFFFF", text_align=ft.TextAlign.CENTER),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[txt_buscar, btn_agregar]
            ),
            ft.Row([contenido], alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True
    )

    mostrar_usuarios()

    contenido_con_fondo = ft.Container(bgcolor="#282728", padding=20, expand=True, content=layout)

    return app_layout(
        page,
        contenido_con_fondo,
        selected_index=2
    )