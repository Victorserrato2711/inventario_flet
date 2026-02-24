import flet as ft
from views.layout import app_layout

def home_view(page, productos, ir_editar, ir_eliminar, ir_agregar,
              ir_categorias, ir_buscar_por_nombre, db, refrescar_home,
              ir_reportes=None, ir_usuarios=None):

    # --- tabla ---
    tabla = ft.DataTable(
        bgcolor="#1E1E1E",
        heading_row_color=ft.Colors.BLUE_GREY_900,
        border=ft.border.all(1, ft.Colors.GREY),
        columns=[
            ft.DataColumn(ft.Text("Id", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Nombre", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Precio", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Cantidad", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Categoría", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Acciones", weight="bold", color=ft.Colors.WHITE)),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(p["id"]), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(p["nombre"], color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(f"${p['precio']:,.2f}", color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(str(p["cantidad"]), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(str(p["categoria_id"]), color=ft.Colors.WHITE)),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                icon_color=ft.Colors.AMBER,
                                on_click=lambda e, pid=p["id"]: ir_editar(pid) if ir_editar else None
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, pid=p["id"], nombre=p["nombre"]: ir_eliminar(pid, nombre) if ir_eliminar else None
                            ),
                        ])
                    ),
                ]
            )
            for p in productos
        ]
    )

    # --- contenido principal ---
    contenido = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Inventario de Productos",
                size=50,
                weight="bold",
                color="#FFFFFF",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Button("Agregar", on_click=ir_agregar, bgcolor="#008000", color="#FFFFFF") if ir_agregar else ft.Text(""),
                    ft.Button("Ver Categorías", on_click=ir_categorias, bgcolor="#0D6EFD", color="#FFFFFF") if ir_categorias else ft.Text(""),
                    ft.TextField(
                        label="Buscar por Nombre",
                        width=300,
                        on_submit=lambda e: ir_buscar_por_nombre(e, tabla, productos) if ir_buscar_por_nombre else None,
                        bgcolor="#1E1E1E",
                        color=ft.Colors.WHITE,
                        cursor_color="#CCCCCC",
                        border_color="#555555",
                        focused_border_color="#888888",
                        focused_bgcolor="#FFFFFF"
                    ),
                ]
            ),
            ft.Container(
                content=tabla,
                expand=False
            )
        ],
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    return app_layout(
        page,
        contenido_con_fondo,
        selected_index=0
    )