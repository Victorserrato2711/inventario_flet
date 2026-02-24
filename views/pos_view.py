from datetime import datetime
from fileinput import filename
import flet as ft
from flet.controls.material.icons import Icons
from services.pos_service import buscar_producto, registrar_venta, generar_ticket, iniciar_turno, retiro_caja, \
    generar_id_venta
from database import Session
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error
from utils.exportar_pdf import exportar_ticket_pdf
from views.layout import app_layout
from decimal import Decimal
from sqlalchemy import text
import re
from decimal import Decimal

def pos_vista(page: ft.Page):
    db = Session()
    productos = []
    total = 0.0
    confirmacion = None  # referencia al cuadro de pago

# ------- Funcionalidades -----------
    def volver_pos(page):
        page.views.clear()
        page.views.append(app_layout(page, contenido_con_fondo, selected_index=4))
        page.update()

    # ----- Inicio de Turno -----
    def mostrar_inicio_turno(e):
        page.views.clear()

        fondo_input = ft.TextField(label="Fondo inicial", value="0")

        def confirmar_inicio(ev):
            usuario_id = getattr(page, "usuario_id", None)
            fondo_inicial = float(fondo_input.value.strip() or "0")
            resultado = iniciar_turno(usuario_id, fondo_inicial)
            if resultado["ok"]:
                mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            else:
                mostrar_mensaje_error(page, resultado["mensaje"])
            volver_pos(page)

        def cancelar_inicio(ev):
            volver_pos(page)

        inicio_view = ft.View(
            route="/inicio_turno",
            controls=[
                ft.Text("Inicio de Turno", size=20, weight="bold", color="#0D47A1"),
                fondo_input,
                ft.Row(
                    controls=[
                        ft.Button("Confirmar", bgcolor="#007BFF", color="white", on_click=confirmar_inicio),
                        ft.Button("Cancelar", bgcolor="#C62828", color="white", on_click=cancelar_inicio)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

        page.views.append(inicio_view)
        page.update()

    btn_inicio_turno = ft.Button(
        "Inicio de Turno",
        icon=ft.Icons.PLAY_ARROW,
        bgcolor="#007BFF",
        color="white",
        on_click=mostrar_inicio_turno
    )

    # ----- Retiro de Caja -----
    def mostrar_retiro(e):
        page.views.clear()

        monto_input = ft.TextField(label="Monto Retiro", value="0")
        motivo_input = ft.TextField(label="Motivo del Retiro")

        def confirmar_retiro(ev):
            usuario_id = getattr(page, "usuario_id", None)
            monto = float(monto_input.value.strip() or "0")
            motivo = motivo_input.value.strip() or "Sin motivo"
            resultado = retiro_caja(usuario_id, monto, motivo)
            if resultado["ok"]:
                mostrar_mensaje(page, resultado["mensaje"], color="#d32f2f")
            else:
                mostrar_mensaje_error(page, resultado["mensaje"])
            volver_pos(page)

        def cancelar_retiro(ev):
            volver_pos(page)

        retiro_view = ft.View(
            route="/retiro",
            controls=[
                ft.Text("Retiro de Caja", size=20, weight="bold", color="#B71C1C"),
                monto_input,
                motivo_input,
                ft.Row(
                    controls=[
                        ft.Button("Confirmar", bgcolor="#C62828", color="white", on_click=confirmar_retiro),
                        ft.Button("Cancelar", bgcolor="#757575", color="white", on_click=cancelar_retiro)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

        page.views.append(retiro_view)
        page.update()

    btn_retiro = ft.Button(
        "Retiro de Caja",
        icon=ft.Icons.MONEY_OFF,
        bgcolor="#C62828",
        color="white",
        on_click=mostrar_retiro
    )

    # ----- Corte de Cierre -----
    def mostrar_corte(e):
        page.views.clear()

        def confirmar_corte(ev):
            from services.pos_service import generar_ticket_corte
            usuario_id = getattr(page, "usuario_id", None)
            ticket_corte = generar_ticket_corte(db, usuario_id)
            filename = f"Corte_{usuario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            exportar_ticket_pdf(ticket_corte, filename=filename, ancho=58)
            mostrar_mensaje(page, "Corte de Caja Generado Correctamente", color="#2E7D32")

            open("retiros.txt", "w").close()

            volver_pos(page)

        def cancelar_corte(ev):
            volver_pos(page)

        corte_view = ft.View(
            route="/corte",
            controls=[
                ft.Text("Corte de Caja", size=20, weight="bold", color="#2E7D32"),
                ft.Row(
                    controls=[
                        ft.Button("Confirmar", bgcolor="#2E7D32", color="white", on_click=confirmar_corte),
                        ft.Button("Cancelar", bgcolor="#C62828", color="white", on_click=cancelar_corte)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

        page.views.append(corte_view)
        page.update()

    btn_corte = ft.Button(
        "Corte de Caja",
        icon=ft.Icons.RECEIPT_LONG,
        bgcolor="#2E7D32",
        color="white",
        on_click=mostrar_corte
    )

    from datetime import datetime

    def calcular_retiros(turno_inicio, turno_fin):
        suma_retiros = 0
        try:
            with open("retiros.txt", "r") as f:
                for linea in f:
                    partes = linea.strip().split(",")
                    if len(partes) < 4:
                        continue
                    usuario_id, monto, motivo, fecha_str = partes
                    fecha = datetime.fromisoformat(fecha_str)
                    if turno_inicio <= fecha <= turno_fin:
                        suma_retiros += float(monto)
        except FileNotFoundError:
            pass
        return suma_retiros

    # ------------ Flujo de Venta --------------------
    codigo_input = ft.TextField(
        label="Código producto",
        on_submit=lambda e: agregar_productos(e),
        autofocus=True
    )
    pago_efectivo_input = ft.TextField(label="Pago en Efectivo", value="0")
    pago_tarjeta_input = ft.TextField(label="Pago con Tarjeta", value="0")

    agregar_btn = ft.Button("Agregar", on_click=lambda e: agregar_productos(e))
    btn_cobrar = ft.Button("Cobrar", on_click=lambda e: mostrar_opciones_pago(e))

    inputs_row = ft.Row(
        controls=[codigo_input, agregar_btn],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- Tabla de productos ---
    tabla_productos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(ft.Text("Producto"), alignment=ft.alignment.Alignment(0, 0))),
            ft.DataColumn(ft.Container(ft.Text("Cantidad"), alignment=ft.alignment.Alignment(0, 0))),
            ft.DataColumn(ft.Container(ft.Text("Precio Unitario"), alignment=ft.alignment.Alignment(0, 0))),
            ft.DataColumn(ft.Container(ft.Text("Subtotal"), alignment=ft.alignment.Alignment(0, 0))),
            ft.DataColumn(ft.Container(ft.Text("Acción"), alignment=ft.alignment.Alignment(0, 0))),
        ],
        rows=[],
        column_spacing=20,
        data_row_min_height=40
    )

    tabla_container = ft.Container(
        content=ft.ListView(controls=[tabla_productos], auto_scroll=False),
        width=600,
        height=300,
        border=ft.border.all(1, "black")
    )

    total_text = ft.Text("Total: $0.00")

    def agregar_productos(e=None):
        nonlocal total
        entrada = codigo_input.value.strip()
        if not entrada:
            return

        match = re.match(r"^(\d+)\s*\*\s*(\d*(?:\.\d+)?)$", entrada)
        if match:
            codigo = match.group(1)
            cantidad_ingresada = Decimal(match.group(2))
        else:
            codigo = entrada  # solo código
            cantidad_ingresada = Decimal("1")

        # Buscar producto por código
        resultado = buscar_producto(db, codigo)
        if not resultado["ok"]:
            mostrar_mensaje_error(page, resultado["mensaje"])
            return

        prod = resultado["producto"]

        existente = next((p for p in productos if p["id"] == prod["id"]), None)
        cantidad_actual = existente["cantidad"] if existente else Decimal("0")

        if prod["cantidad"] < cantidad_actual + cantidad_ingresada:
            mostrar_mensaje_error(page, f"Stock insuficiente. Disponible: {prod['cantidad']}")
            return

        if existente:
            existente["cantidad"] += cantidad_ingresada
        else:
            productos.append({
                "id": prod["id"],
                "cantidad": cantidad_ingresada,
                "precio": prod["precio"],
                "nombre": prod["nombre"]
            })

        total = sum(p["cantidad"] * p["precio"] for p in productos)
        total_text.value = f"Total: ${total:,.2f}"

        tabla_productos.rows.clear()
        for p in productos:
            fila = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Container(ft.Text(p["nombre"]), alignment=ft.alignment.Alignment(0, 0))),
                    ft.DataCell(ft.Container(ft.Text(f"{p['cantidad']:.3f}"), alignment=ft.alignment.Alignment(0, 0))),
                    ft.DataCell(ft.Container(ft.Text(f"${p['precio']:,.2f}"), alignment=ft.alignment.Alignment(0, 0))),
                    ft.DataCell(
                        ft.Container(ft.Text(f"${p['cantidad'] * p['precio']:,.2f}"),
                                     alignment=ft.alignment.Alignment(0, 0))
                    ),
                    ft.DataCell(
                        ft.Container(
                            ft.Button("❌", on_click=lambda ev, prod=p: cancelar_producto(prod)),
                            alignment=ft.alignment.Alignment(0, 0)
                        )
                    )
                ]

            )
            tabla_productos.rows.append(fila)

        mostrar_mensaje(page, "Producto agregado correctamente", color="#28a745")
        codigo_input.value = ""
        codigo_input.focus()
        page.update()

    def cancelar_producto(producto):
        nonlocal total
        if producto in productos:
            productos.remove(producto)
            total = sum(p["cantidad"] * p["precio"] for p in productos)
            total_text.value = f"Total: ${total:,.2f}"

            tabla_productos.rows.clear()
            for p in productos:
                fila = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p["nombre"])),
                        ft.DataCell(ft.Text(f"{p['cantidad']:.2f}")),
                        ft.DataCell(ft.Text(f"${p['precio']:,.2f}")),
                        ft.DataCell(ft.Text(f"${p['cantidad'] * p['precio']:,.2f}")),
                        ft.DataCell(ft.Button("❌", on_click=lambda ev, prod=p: cancelar_producto(prod)))
                    ]
                )
                tabla_productos.rows.append(fila)

            mostrar_mensaje(page, f"Producto '{producto['nombre']}' eliminado", color="#ffc107")
            codigo_input.focus()
            page.update()
        else:
            mostrar_mensaje_error(page, "Producto no encontrado en la venta")
            codigo_input.focus()
            page.update()

    def registrar_venta(db, usuario_id, total, metodo_pago):
        try:
            id_venta = generar_id_venta(db)

            db.execute(
                text("""
                    INSERT INTO ventas (id_venta, usuario_id, fecha, total, metodo_pago)
                    VALUES (:id_venta, :usuario_id, NOW(), :total, :metodo_pago)
                """),
                {
                    "id_venta": id_venta,
                    "usuario_id": usuario_id,
                    "total": total,
                    "metodo_pago": metodo_pago
                }
            )
            db.commit()

            return {"ok": True, "mensaje": f"Venta registrada con ID {id_venta}"}
        except Exception as e:
            db.rollback()
            return {"ok": False, "mensaje": str(e)}

    def registrar_detalle_venta(db, venta_id, producto_id, nombre_producto, cantidad, precio_unitario):
        try:
            db.execute(
                text("""
                    INSERT INTO detalle_ventas (id_venta, producto_id, nombre_producto, cantidad, precio_unitario)
                    VALUES (:venta_id, :producto_id, :nombre_producto, :cantidad, :precio_unitario)
                """),
                {
                    "venta_id": venta_id,
                    "producto_id": producto_id,
                    "nombre_producto": nombre_producto,
                    "cantidad": float(cantidad),
                    "precio_unitario": float(precio_unitario)
                }
            )
            db.commit()
            return {"ok": True, "mensaje": "Detalle registrado"}
        except Exception as e:
            db.rollback()
            return {"ok": False, "mensaje": str(e)}

    boton_imprimir = ft.Button(
        "Imprimir Ticket",
        icon=ft.Icons.PRINT,
        visible=False
    )

    def finalizar_venta(e=None):
        nonlocal total, confirmacion
        try:
            pago_efectivo = Decimal(pago_efectivo_input.value.strip() or "0")
            pago_tarjeta = Decimal(pago_tarjeta_input.value.strip() or "0")
        except Exception:
            mostrar_mensaje_error(page, "Los valores de pago deben ser numéricos")
            codigo_input.focus()  # 🔹 devuelve el foco en caso de error
            page.update()
            return

        monto_entregado = pago_efectivo + pago_tarjeta
        if monto_entregado < total:
            mostrar_mensaje_error(page, "El monto entregado es insuficiente")
            codigo_input.focus()  # 🔹 devuelve el foco en caso de error
            page.update()
            return

        cambio = monto_entregado - total if pago_efectivo > 0 else Decimal("0.00")

        metodo_pago = []
        if pago_efectivo > 0:
            metodo_pago.append("Efectivo")
        if pago_tarjeta > 0:
            metodo_pago.append("Tarjeta")

        usuario_id = getattr(page, "usuario_id", None)
        resultado = registrar_venta(
            db,
            usuario_id=usuario_id,
            total=float(total),
            metodo_pago="+".join(metodo_pago)
        )
        if not resultado["ok"]:
            mostrar_mensaje_error(page, resultado["mensaje"])
            codigo_input.focus()  # 🔹 devuelve el foco en caso de error
            page.update()
            return

        id_venta = resultado["mensaje"].split()[-1]

        for p in productos:
            detalle_res = registrar_detalle_venta(
                db,
                venta_id=id_venta,
                producto_id=p["id"],
                nombre_producto=p["nombre"],
                cantidad=p["cantidad"],
                precio_unitario=p["precio"]
            )
            if not detalle_res["ok"]:
                mostrar_mensaje_error(page, detalle_res["mensaje"])
                codigo_input.focus()  # 🔹 devuelve el foco en caso de error
                page.update()
                return

        ticket = generar_ticket(
            id_venta,
            db,
            total=float(total),
            metodo_pago="+".join(metodo_pago),
            monto_entregado=monto_entregado,
            cambio=cambio
        )

        filename = f"Ticket_{id_venta}.pdf"
        exportar_ticket_pdf(ticket, filename=filename, ancho=58)

        mostrar_mensaje(page, f"Venta registrada con éxito. Cambio: ${float(cambio):.2f}", color="#28a745")

        boton_imprimir.on_click = lambda e: ocultar_boton_despues_de_imprimir(filename)
        boton_imprimir.visible = True

        productos.clear()
        tabla_productos.rows.clear()
        total = Decimal("0.00")
        total_text.value = "Total: $0.00"
        quitar_confirmacion()
        codigo_input.focus()
        page.update()

    def quitar_confirmacion(e=None):
        nonlocal confirmacion
        if confirmacion in page.overlay:
            page.overlay.remove(confirmacion)
            page.update()
            codigo_input.focus()  # 🔹 devuelve el foco al campo al cerrar el overlay
            page.update()

    def mostrar_opciones_pago(e):
        nonlocal confirmacion
        if not productos:
            mostrar_mensaje_error(page, "No hay productos a la venta")
            codigo_input.focus()  # 🔹 devuelve el foco si no hay productos
            page.update()
            return

        pago_efectivo_input.value = "0"
        pago_tarjeta_input.value = "0"

        confirmacion = ft.Container(
            bgcolor=ft.Colors.BLACK,
            padding=20,
            width=300,
            height=250,
            alignment=ft.alignment.Alignment(1, 0),
            content=ft.Column(
                controls=[
                    ft.Text("Método de Pago", color="WHITE", size=20, weight="bold"),
                    pago_efectivo_input,
                    pago_tarjeta_input,
                    ft.Row(
                        controls=[
                            ft.Button("Confirmar", bgcolor="#28a745", color="WHITE", on_click=finalizar_venta),
                            ft.Button("Cancelar", bgcolor="#dc3545", color="WHITE", on_click=quitar_confirmacion)
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.END
            )
        )

        page.overlay.append(confirmacion)
        page.update()

    def ocultar_boton_despues_de_imprimir(filename):
        page.launch_url(filename)
        boton_imprimir.visible = False
        codigo_input.focus()
        page.update()

    # ---- Componentes de la vista principal ----
    acciones_superiores = ft.Row(
        spacing=10,
        controls=[agregar_btn, btn_inicio_turno, btn_retiro, btn_corte]
    )

    contenido = ft.Column(
        spacing=20,
        controls=[
            inputs_row,
            acciones_superiores,
            tabla_container,
            total_text,
            btn_cobrar,
            boton_imprimir
        ]
    )

    contenido_con_fondo = ft.Container(
        bgcolor="#282728",
        expand=True,
        content=contenido
    )

    return app_layout(page, contenido_con_fondo, selected_index=5)

