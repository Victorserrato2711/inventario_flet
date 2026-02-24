import flet as ft
from sqlalchemy import text
from services.entradas_service import registrar_entrada
from views.layout import app_layout
from utils.exportar_pdf import exportar_ticket_pdf
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error


# --- Generar Ticket de Entrada ---
def generar_ticket_entrada(db, id_entrada: str):
    entrada = db.execute(
        text("""
            SELECT id_entrada, usuario_nombre, fecha_registro, total_productos, total_unidades
            FROM entradas WHERE id_entrada = :id
        """),
        {"id": id_entrada}
    ).fetchone()

    if not entrada:
        return "No se encontró la entrada"

    detalles = db.execute(
        text("SELECT producto_id, nombre_producto, cantidad FROM detalle_entradas WHERE id_entrada = :id"),
        {"id": id_entrada}
    ).fetchall()

    lineas = [
        "---- Ticket de Entrada ----",
        f"ID Entrada: {entrada.id_entrada}",
        f"Fecha: {entrada.fecha_registro}",
        f"Registró: {entrada.usuario_nombre}",
        "--------------------------------------------------"
    ]

    for d in detalles:
        lineas.append(f"{d.nombre_producto} x{d.cantidad}")

    lineas.append("--------------------------------------------------")
    lineas.append(f"Total Productos: {entrada.total_productos}")
    lineas.append(f"Total Unidades: {entrada.total_unidades}")
    lineas.append("==================================================")
    lineas.append("Gracias por su entrega. Este comprobante es válido para aclaraciones.")

    return "\n".join(lineas)   # ✅ devolvemos string


# --- Pantalla Principal de Entradas ---
def ver_entradas(page: ft.Page, ir_home, ir_registro, db, refrescar_home):
    usuario_id = getattr(page, "usuario_id", None)

    filtro_id = ft.TextField(label="Buscar Id Entrada", width=250)

    boton_registrar = ft.Button(
        "Registrar Entrada",
        on_click=lambda e: ir_registro(),
        bgcolor="#0D6EFD",
        color="#FFFFFF"
    )

    # --- Tabla ---
    tabla_detalle = ft.DataTable(
        heading_row_color=ft.Colors.BLUE_GREY_900,
        border=ft.border.all(1, ft.Colors.GREY),
        columns=[
            ft.DataColumn(ft.Text("Id de Entrada", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Producto Id", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Nombre Producto", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Cantidad", weight="bold", color=ft.Colors.WHITE)),
        ],
        rows=[]
    )

    # --- Función para cargar datos ---
    def cargar_datos(id_filtro=None):
        if id_filtro:
            registros = db.execute(
                text("""SELECT d.id_entrada, d.producto_id, d.nombre_producto, d.cantidad
                        FROM detalle_entradas d
                        WHERE d.id_entrada = :id"""),
                {"id": id_filtro}
            ).fetchall()
        else:
            registros = db.execute(
                text("""SELECT d.id_entrada, d.producto_id, d.nombre_producto, d.cantidad
                        FROM detalle_entradas d""")
            ).fetchall()

        tabla_detalle.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(r.id_entrada))),
                    ft.DataCell(ft.Text(str(r.producto_id))),
                    ft.DataCell(ft.Text(r.nombre_producto)),
                    ft.DataCell(ft.Text(str(r.cantidad))),
                ]
            )
            for r in registros
        ]
        page.update()

    # --- Botón buscar ---
    boton_buscar = ft.Button(
        "Buscar",
        on_click=lambda e: cargar_datos(filtro_id.value.strip()),
        bgcolor="#198754",
        color="#FFFFFF"
    )

    barra_filtros = ft.Row(
        controls=[filtro_id, boton_buscar, boton_registrar],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # --- Contenido ---
    contenido = ft.Column(
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Entradas", size=30, color="white"),
            barra_filtros,
            ft.Container(content=tabla_detalle, padding=20, border_radius=10, bgcolor="#1E1E1E"),
            ft.Button("Volver", on_click=lambda e: ir_home(), bgcolor="#6C757D", color="WHITE")
        ],
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    cargar_datos()

    return app_layout(page, contenido_con_fondo, selected_index=5)


# --- Registrar Entrada ---
def registrar_entradas_vista(page, volver, db, refrescar_home):
    campo_codigo = ft.TextField(label="Código del Producto", width=200)
    campo_cantidad = ft.TextField(label="Cantidad", width=200)

    tabla_detalle = ft.DataTable(
        heading_row_color=ft.Colors.BLUE_GREY_900,
        border=ft.border.all(1, ft.Colors.GREY),
        columns=[
            ft.DataColumn(ft.Text("Producto Id", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Producto", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Cantidad", weight="bold", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Acciones", weight="bold", color=ft.Colors.WHITE))
        ],
        rows=[]
    )

    productos_temp = []

    def eliminar_producto_temp(codigo):
        nonlocal productos_temp
        productos_temp = [p for p in productos_temp if p["producto_id"] != codigo]
        tabla_detalle.rows = [
            row for row in tabla_detalle.rows if row.cells[0].content.value != str(codigo)
        ]
        page.update()

    def agregar_producto(e):
        codigo = campo_codigo.value.strip()
        cantidad = campo_cantidad.value.strip()

        if not codigo or not cantidad.isdigit():
            mostrar_mensaje_error(page, "Debe ingresar un código y una cantidad válida")
            return

        cantidad = int(cantidad)

        result_prod = db.execute(
            text("SELECT nombre FROM productos WHERE id = :producto_id"),
            {"producto_id": codigo}
        ).fetchone()

        if not result_prod:
            mostrar_mensaje_error(page, f"Producto con ID {codigo} no existe")
            return
        nombre_producto = result_prod[0]

        productos_temp.append({
            "producto_id": codigo,
            "nombre": nombre_producto,
            "cantidad": cantidad
        })

        tabla_detalle.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(codigo))),
                    ft.DataCell(ft.Text(nombre_producto)),
                    ft.DataCell(ft.Text(str(cantidad))),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_400,
                            tooltip="Eliminar",
                            on_click=lambda ev, cid=codigo: eliminar_producto_temp(cid)
                        )
                    ),
                ]
            )
        )
        campo_codigo.value = ""
        campo_cantidad.value = ""
        page.update()

    def guardar_entrada(e):
        if not productos_temp:
            mostrar_mensaje_error(page, "Debe agregar al menos un producto")
            return

        usuario_id = getattr(page, "usuario_id", None)
        resultado = registrar_entrada(db, usuario_id, productos_temp)

        if resultado["ok"]:
            mostrar_mensaje(page, resultado["mensaje"], color="#28a745")

            # ✅ Generar ticket como string
            ticket_text = generar_ticket_entrada(db, resultado["id_entrada"])
            filename = f"Entrada_{resultado['id_entrada']}.pdf"
            exportar_ticket_pdf(ticket_text, filename=filename, ancho=58)

            refrescar_home()
            volver()
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    boton_agregar = ft.Button("Agregar", on_click=agregar_producto, bgcolor="#008000", color="#FFFFFF")
    boton_guardar = ft.Button("Guardar Entrada", on_click=guardar_entrada, bgcolor="#0D6EFD", color="#FFFFFF")
    boton_volver = ft.Button("Volver", on_click=lambda e: volver(), bgcolor="#6C757D", color="#FFFFFF")

    contenido = ft.Column(
        [
            ft.Text("Registrar Entrada", size=25, color="white"),
            ft.Row([campo_codigo, campo_cantidad, boton_agregar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(content=tabla_detalle, padding=20, border_radius=10, bgcolor="#1E1E1E"),
            ft.Row([boton_guardar, boton_volver], alignment=ft.MainAxisAlignment.CENTER)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    return app_layout(page, contenido_con_fondo, selected_index=5)