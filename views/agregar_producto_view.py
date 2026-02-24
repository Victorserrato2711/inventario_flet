import flet as ft
from sqlalchemy.testing.plugin.plugin_base import options

from services.producto_service import crear_producto
from services.categoria_service import listado_categorias
from utils.mensajes import mostrar_mensaje_error, mostrar_mensaje
from views.layout import app_layout

def agregar_producto_view(page: ft.Page, ir_home, db, refrescar_home):
    id_field = ft.TextField(label="Id")
    nombre_field = ft.TextField(label="Nombre")
    precio_field = ft.TextField(label="Precio")
    cantidad_field = ft.TextField(label="Cantidad")

    resultado = listado_categorias(db)
    if resultado["ok"]:
        categorias = resultado["categorias"]
    else:
        categorias = []

    opciones_categoria = [
        ft.dropdown.Option(str(c["id"]), text=c["nombre"]) for c in categorias
    ]

    categoria_field = ft.Dropdown(label="Categoria", options=opciones_categoria)

    def on_guardar(ev):
        try:
            datos = {
                "id": int(id_field.value),
                "nombre": nombre_field.value.strip(),
                "precio": float(precio_field.value),
                "cantidad": int(cantidad_field.value),
                "categoria_id": int(categoria_field.value),
            }
        except Exception:
            mostrar_mensaje_error(page,"Datos Invalidos")
            return

        resultado = crear_producto(db, datos)

        if resultado["ok"]:
            mostrar_mensaje(page,resultado["mensaje"],color="#28a745")
            refrescar_home()
            page.go("/home")
        else:
            mostrar_mensaje_error(page,resultado["mensaje"])

    contenido = ft.Column(
        [
            ft.Text("Agregar Producto", size=25, color="#FFFFFF"),
            id_field,
            nombre_field,
            precio_field,
            cantidad_field,
            categoria_field,
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
                        on_click=lambda e: ir_home(),
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
        selected_index=0
    )