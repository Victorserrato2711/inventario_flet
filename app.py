import flet as ft
import socket
from services.salir_service import logout_usuario
from views.login import login_view
from views.cambio_contraseña_login_view import cambio_contraseña_login_view
from services.producto_service import listado_productos, eliminar_producto
from database import get_db
from views.home_view import home_view
from views.layout import app_layout
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error
import models
from views.entradas_view import ver_entradas, registrar_entradas_vista



def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


async def main(page: ft.Page):
    page.title = "Inventario Flet"
    page.bgcolor = "#282728"
    db = get_db()

    # --- Busqueda por Nombre ---
    def ir_buscar_por_nombre(e, tabla, productos):
        texto = e.control.value.strip().lower()
        if texto == "":
            refrescar_home()
            return

        filtrados = [p for p in productos if texto in p["nombre"].lower()]
        page.views.clear()
        page.views.append(
            home_view(
                page,
                filtrados,
                ir_editar,
                ir_eliminar,
                ir_agregar,
                ir_categorias,
                ir_buscar_por_nombre,
                db,
                refrescar_home
            )
        )
        page.update()

    # --- Barra lateral ---
    def ir_entradas():
        page.views.clear()
        page.views.append(
            ver_entradas(
                page,
                lambda: ir_home(),
                lambda: mostrar_registro_entradas(page, db),  # ya no pasamos usuario_id
                db,
                lambda: ir_entradas()  # refrescar_home
            )
        )
        page.update()

    def ir_pos(e=None):
        from views.pos_view import pos_vista
        page.views.clear()
        page.views.append(pos_vista(page))
        page.update()

    def ir_reportes(e=None):
        from views.reportes_view import reportes_view
        page.views.clear()
        page.views.append(reportes_view(page, db, refrescar_home))
        page.update()

    def ir_usuarios(e=None):
        from views.usuarios_view import usuario_view
        page.views.clear()
        page.views.append(usuario_view(page, db, refrescar_home))
        page.update()

    def ir_cambio_contrasena(e=None):
        from views.cambio_contraseña_view import cambiar_contraseña_view
        page.views.clear()
        page.views.append(cambiar_contraseña_view(page, db, refrescar_usuarios=ir_usuarios))
        page.update()

    # --- Eliminar Categoría ---
    def ir_eliminar_categoria(id_categoria, nombre_categoria):
        from services.categoria_service import eliminar_categoria

        def ejecutar_eliminacion(cid):
            resultado = eliminar_categoria(db, cid)
            quitar_confirmacion()
            refrescar_home()

            if resultado["ok"]:
                mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            else:
                mostrar_mensaje_error(page, resultado["mensaje"])

        def quitar_confirmacion():
            page.controls.remove(confirmacion)
            page.update()

        confirmacion = ft.Container(
            bgcolor=ft.Colors.BLACK,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"¿Seguro que deseas eliminar la categoría '{nombre_categoria}'?",
                        color="WHITE"
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                "Sí, Eliminar",
                                bgcolor="#DC3545",
                                color="WHITE",
                                on_click=lambda e: ejecutar_eliminacion(id_categoria)
                            ),
                            ft.Button(
                                "Cancelar",
                                bgcolor="#6C757D",
                                color="WHITE",
                                on_click=lambda e: quitar_confirmacion()
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

    # --- Editar Categoría ---
    def ir_editar_categoria(id_categoria):
        from views.categorias_view import editar_categoria_vista
        page.views.clear()
        page.views.append(
            editar_categoria_vista(page, lambda: ir_categorias(), id_categoria, db, refrescar_home)
        )
        page.update()

    # --- Eliminar Producto ---
    def ir_eliminar(id_producto, nombre_producto):
        def ejecutar_eliminacion(pid):
            resultado = eliminar_producto(db, pid)
            quitar_confirmacion()
            refrescar_home()

            if resultado["ok"]:
                mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            else:
                mostrar_mensaje_error(page, resultado["mensaje"])

        def quitar_confirmacion():
            page.controls.remove(confirmacion)
            page.update()

        confirmacion = ft.Container(
            bgcolor=ft.Colors.BLACK,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"¿Seguro que deseas eliminar el producto '{nombre_producto}'?",
                        color="WHITE"
                    ),
                    ft.Row(
                        controls=[
                            ft.Button(
                                "Sí, Eliminar",
                                bgcolor="#DC3545",
                                color="WHITE",
                                on_click=lambda e: ejecutar_eliminacion(id_producto)
                            ),
                            ft.Button(
                                "Cancelar",
                                bgcolor="#6C757D",
                                color="WHITE",
                                on_click=lambda e: quitar_confirmacion()
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

    # ---- Agregar Entradas ----
    def mostrar_entradas(page, db):
        page.views.clear()
        page.views.append(
            ver_entradas(
                page,
                lambda: ir_home(),
                lambda: mostrar_registro_entradas(page, db),
                db,
                lambda: mostrar_entradas(page, db)
            )
        )
        page.update()

    def mostrar_registro_entradas(page, db):
        page.views.clear()
        page.views.append(
            registrar_entradas_vista(
                page,
                lambda: mostrar_entradas(page, db),
                db,
                lambda: mostrar_entradas(page, db)
            )
        )
        page.update()

    # --- Editar Producto ---
    def ir_editar(id_producto):
        from views.editar_producto_view import editar_producto_vista
        page.views.clear()
        page.views.append(
            editar_producto_vista(page, id_producto, refrescar_home, db, refrescar_home)
        )
        page.update()

    # --- Agregar Categoría ---
    def ir_agregar_categorias(page, volver, db, refrescar_home):
        from views.categorias_view import agregar_categoria_vista
        page.views.clear()
        page.views.append(
            agregar_categoria_vista(page, lambda: ir_categorias(), db, refrescar_home)
        )
        page.update()

    # --- Refrescar Home ---
    def refrescar_home(e=None):
        resultado = listado_productos(db)
        productos = resultado["productos"] if resultado["ok"] else []
        page.views.clear()
        page.views.append(
            home_view(
                page,
                productos,
                ir_editar,
                ir_eliminar,
                ir_agregar,
                ir_categorias,
                ir_buscar_por_nombre,
                db,
                refrescar_home
            )
        )
        page.update()

    # --- Agregar Producto ---
    def ir_agregar(e=None):
        from views.agregar_producto_view import agregar_producto_view
        page.views.clear()
        page.views.append(agregar_producto_view(page, refrescar_home, db, refrescar_home))
        page.update()

    # --- Categorías ---
    def ir_categorias(e=None):
        from views.categorias_view import ver_categorias
        page.views.clear()
        page.views.append(
            ver_categorias(page, refrescar_home, ir_agregar_categorias, ir_editar_categoria, ir_eliminar_categoria, db, refrescar_home)
        )
        page.update()

    # ----- Manejos de Rutas -----
    async def route_change(e, usuario_id=None):
        rutas_protegidas = [
            "/home",
            "/reportes",
            "/usuarios",
            "/cambiar_contraseña",
            "/pos",
            "/entradas"  # 🔹 nueva ruta protegida
        ]
        if page.route in rutas_protegidas and not getattr(page, "usuario_id", None):
            page.go("/login")
            return

        if page.route == "/login":
            page.views.clear()
            page.views.append(
                ft.View(
                    route="/login",
                    expand=True,
                    bgcolor="#282728",
                    controls=[login_view(page, db)]
                )
            )
            page.update()

        elif page.route.startswith("/cambio_contraseña_login"):
            usuario = page.route.split("?usuario=")[-1]
            page.views.clear()
            page.views.append(
                ft.View(
                    route="/cambio_contraseña_login",
                    expand=True,
                    bgcolor="#282728",
                    controls=[cambio_contraseña_login_view(page, usuario, db)]
                )
            )
            page.update()

        elif page.route == "/home":
            resultado = listado_productos(db)
            productos = resultado["productos"] if resultado["ok"] else []
            page.views.clear()
            page.views.append(
                home_view(
                    page,
                    productos,
                    ir_editar,
                    ir_eliminar,
                    ir_agregar,
                    ir_categorias,
                    ir_buscar_por_nombre,
                    db,
                    refrescar_home
                )
            )
            page.update()

        elif page.route == "/reportes":
            ir_reportes()

        elif page.route == "/usuarios":
            ir_usuarios()

        elif page.route == "/cambiar_contraseña":
            ir_cambio_contrasena()

        elif page.route == "/pos":
            ir_pos()

        elif page.route == "/entradas":
            mostrar_entradas(page, db)

        elif page.route == "/logout":
            logout_service(page, db)

    def logout_service(page, db):
        setattr(page, "usuario_id", None)
        resultado = logout_usuario()

        if not resultado["ok"]:
            mostrar_mensaje_error(page, resultado["mensaje"])

        try:
            db.close()
        except Exception as ex:
            mostrar_mensaje_error(page, f"Error al Cerrar Sesión: {ex}")

        new_db = get_db()
        page.views.clear()
        page.views.append(
            ft.View(
                route="/login",
                expand=True,
                bgcolor="#282728",
                controls=[login_view(page, new_db)]
            )
        )
        page.update()

    page.on_route_change = route_change

    # --- carga inicial ---
    await page.push_route("/login")


if __name__ == "__main__":
    ip_local = get_local_ip()
    print("===================================================")
    print("🚀 Servidor Flet ejecutándose…")
    print("📌 Accede desde este navegador:")
    print(f"👉 http://{ip_local}:8560")
    print("===================================================")

    ft.run(
        main,
        host=f"{ip_local}",
        port=8560,
        view=ft.AppView.FLET_APP_WEB
    )
