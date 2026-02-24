import flet as ft
from services.categoria_service import (
    crear_categoria,
    consulta_id_categoria,
    listado_categorias,
    actualizar_categoria,
    eliminar_categoria,
)
from utils.mensajes import mostrar_mensaje_error, mostrar_mensaje
from views.layout import app_layout


# --- Editar Categoría ---
def editar_categoria_vista(page, volver, categoria_id, db, refrescar_home):
    resultado = consulta_id_categoria(db, categoria_id)
    if not resultado["ok"]:
        mostrar_mensaje_error(page, resultado["mensaje"])
        return

    categoria = resultado["categoria"]

    id_field = ft.TextField(label="Id", value=str(categoria["id"]), disabled=True, color="White")
    nombre_field = ft.TextField(label="Nombre", value=categoria["nombre"], bgcolor="#FFFFFF", color="Black")

    def on_guardar(e):
        if not nombre_field.value.strip():
            mostrar_mensaje_error(page, "Debe llenar el campo Nombre")
            return

        resultado = actualizar_categoria(db, id_field.value, nombre_field.value.strip())
        if resultado["ok"]:
            mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            volver()
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    contenido = ft.Column(
        [
            ft.Text("Editar Categoría", size=25, color="white"),
            id_field,
            nombre_field,
            ft.Row([
                ft.Button("Guardar", on_click=on_guardar, bgcolor="#008000", color="#FFFFFF"),
                ft.Button("Volver", on_click=lambda e: volver(), bgcolor="#6C757D", color="#FFFFFF")
            ])
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    return app_layout(page, contenido_con_fondo, selected_index=0)


# --- Pantalla Principal de Categorías ---
def ver_categorias(page: ft.Page, ir_home, ir_agregar_categoria, ir_editar_categoria, ir_eliminar_categoria, db, refrescar_home):
    resultado = listado_categorias(db)
    categorias = resultado["categorias"] if resultado["ok"] else []

    if not categorias:
        contenido = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("No hay categorías registradas", color="red"),
                ft.Button("Volver", on_click=lambda e: ir_home(), bgcolor="#6C757D", color="WHITE")
            ],
            expand=True
        )
        contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)
        return app_layout(page, contenido_con_fondo, selected_index=0)

    tabla = ft.DataTable(
        bgcolor="#1E1E1E",
        heading_row_color=ft.Colors.BLUE_GREY_900,
        border=ft.border.all(1, ft.Colors.GREY),
        columns=[
            ft.DataColumn(ft.Text("Id")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(c["id"]))),
                    ft.DataCell(ft.Text(c["nombre"])),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                icon_color=ft.Colors.AMBER,
                                on_click=lambda e, cid=c["id"]: ir_editar_categoria(cid) if ir_editar_categoria else None
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Eliminar",
                                on_click=lambda e, cid=c["id"], nombre=c["nombre"]: ir_eliminar_categoria(cid, nombre) if ir_eliminar_categoria else None
                            ),
                        ])
                    ),
                ]
            )
            for c in categorias
        ]
    )

    contenido = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Gestión de Categorías", size=30, color="white"),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Button(
                        "Agregar",
                        on_click=lambda e: ir_agregar_categoria(
                            page,
                            lambda: ver_categorias(page, ir_home, ir_agregar_categoria, ir_editar_categoria, ir_eliminar_categoria, db, refrescar_home),
                            db,
                            refrescar_home
                        ),
                        bgcolor="#008000",
                        color="WHITE"
                    ),
                    ft.Button("Volver", on_click=lambda e: ir_home(), bgcolor=ft.Colors.GREY, color="WHITE")
                ]
            ),
            ft.Row([tabla], alignment=ft.MainAxisAlignment.CENTER)
        ],
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    return app_layout(page, contenido_con_fondo, selected_index=0)


# --- Agregar Categoría ---
def agregar_categoria_vista(page, volver, db, refrescar_home):
    id_field = ft.TextField(label="Id")
    nombre_field = ft.TextField(label="Nombre")

    def on_guardar(e):
        if not id_field.value.strip() or not nombre_field.value.strip():
            mostrar_mensaje_error(page, "Debe llenar todos los campos")
            return

        resultado = crear_categoria(db, id_field.value.strip(), nombre_field.value.strip())
        if resultado["ok"]:
            mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            volver()
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    contenido = ft.Column(
        [
            ft.Text("Agregar Categoría", size=25, color="white"),
            id_field,
            nombre_field,
            ft.Row(
                controls=[
                    ft.Button("Guardar", on_click=on_guardar, bgcolor="#008000", color="#FFFFFF"),
                    ft.Button("Volver", on_click=lambda e: volver(), bgcolor="#6C757D", color="#FFFFFF"),
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
        selected_index=0
    )