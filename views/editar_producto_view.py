import flet as ft
from services.producto_service import consulta_id_producto, actualizar_producto
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error
from views.layout import app_layout
from models import Categoria

def editar_producto_vista(page: ft.Page, id_producto: int, ir_home, db, refrescar_home):
    resultado = consulta_id_producto(db, int(id_producto))

    if not resultado["ok"]:
        contenido = ft.Column(
            [
                ft.Text("Error al cargar producto", color="red", size=20),
                ft.Text(resultado["mensaje"]),
                ft.Button("Volver", on_click=lambda e: ir_home(), bgcolor="#6C757D", color="WHITE")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
        contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)
        return app_layout(page, contenido_con_fondo, selected_index=0)

    producto = resultado["producto"]

    # Campos básicos
    nombre_field = ft.TextField(label="Nombre", value=producto["nombre"])
    precio_field = ft.TextField(label="Precio", value=str(producto["precio"]))
    cantidad_field = ft.TextField(label="Cantidad", value=str(producto["cantidad"]))

    # Dropdown de categorías
    categorias = db.query(Categoria).all()
    categoria_dropdown = ft.Dropdown(
        label="Categoría",
        options=[ft.dropdown.Option(str(c.id), text=c.nombre) for c in categorias],
        value=str(producto["categoria_id"]),  # preselecciona la categoría actual
        text_style=ft.TextStyle(color="white"),
        fill_color="#333333",
        border_color="blue",
        focused_border_color="green"
    )

    def on_guardar(e):
        if not nombre_field.value.strip() or not precio_field.value.strip() or not cantidad_field.value.strip() or not categoria_dropdown.value:
            mostrar_mensaje_error(page, "Debe llenar todos los campos")
            return
        try:
            precio = float(precio_field.value)
            cantidad = int(cantidad_field.value)
            categoria = int(categoria_dropdown.value)
        except ValueError:
            mostrar_mensaje_error(page, "Precio, cantidad y categoría deben ser numéricos")
            return

        # Actualizar producto
        resultado = actualizar_producto(
            db,
            int(id_producto),
            nombre_field.value.strip(),
            precio,
            cantidad,
            categoria
        )
        if resultado["ok"]:
            mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            refrescar_home()
            ir_home()
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    contenido = ft.Column(
        [
            ft.Text("Editar Producto", size=25, color="#FFFFFF"),
            nombre_field,
            precio_field,
            cantidad_field,
            categoria_dropdown,
            ft.Row([
                ft.Button("Guardar", on_click=on_guardar, bgcolor="#008000", color="#FFFFFF"),
                ft.Button("Volver", on_click=lambda e: ir_home(), bgcolor="#6C757D", color="#FFFFFF")
            ])
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