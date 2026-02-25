import flet as ft
from utils.mensajes import mostrar_mensaje, mostrar_mensaje_error
from views.layout import app_layout
from services.reporte_service import (
    reporte_productos_por_categoria,
    reporte_stock_bajo,
    reporte_valor_inventario,
    reporte_administrativo_productos,
    exportar_csv,
    exportar_excel
)

def reportes_view(page: ft.Page, db, refrescar_home):
    link_container = ft.Column()    

    reportes_dropdown = ft.Dropdown(
        label="Selecciona un reporte",
        options=[
            ft.dropdown.Option("Productos por Categoria"),
            ft.dropdown.Option("Stock Bajo"),
            ft.dropdown.Option("Valor del Inventario"),
            ft.dropdown.Option("Administrativo")
        ],
        text_style=ft.TextStyle(color="white"),
        fill_color="#333333",
        border_color="blue",
        focused_border_color="green"
    )

    def mostrar_link(resultado):
        async def volver_reportes(e):
            await page.launch_url(f"/reports/{resultado['archivo']}")
            page.views.clear()
            page.views.append(reportes_view(page, db, refrescar_home))
            page.update()

        link_container.controls.clear()
        link_container.controls.append(
            ft.TextButton(
                content=ft.Text(f"Descargar {resultado['archivo']}", color="blue"),
                url=f"/reports/{resultado['archivo']}",
                on_click=volver_reportes
            )
        )
        page.update()

    def on_exportar_csv(e):
        if not reportes_dropdown.value:
            mostrar_mensaje_error(page, "Debe seleccionar un reporte")
            return

        if reportes_dropdown.value == "Productos por Categoria":
            datos = reporte_productos_por_categoria(db)
            encabezados_visibles = ["Categoría", "Total"]
            claves = ["categoria_nombre", "total"]
            resultado = exportar_csv("categorias.csv", encabezados_visibles, claves, datos)

        elif reportes_dropdown.value == "Stock Bajo":
            datos = reporte_stock_bajo(db)
            encabezados_visibles = ["Id", "Nombre", "Cantidad"]
            claves = ["id", "nombre", "cantidad"]
            resultado = exportar_csv("stock_bajo.csv", encabezados_visibles, claves, datos)

        elif reportes_dropdown.value == "Valor del Inventario":
            datos = reporte_valor_inventario(db)
            encabezados_visibles = ["Id", "Nombre", "Cantidad", "Categoría", "Valor Total"]
            claves = ["id", "nombre", "cantidad", "categoria_nombre", "total"]
            resultado = exportar_csv("valor_inventario.csv", encabezados_visibles, claves, datos)

        elif reportes_dropdown.value == "Administrativo":
            datos = reporte_administrativo_productos(db)
            encabezados_visibles = ["Id", "Nombre", "Cantidad", "Precio Unitario", "Valor Total",
                                    "Categoría", "Fecha de Creación"]
            claves = ["id", "nombre", "cantidad", "precio", "total", "categoria_nombre", "fecha_creacion"]
            resultado = exportar_csv("administrativo_general.csv", encabezados_visibles, claves, datos)

        if resultado["ok"]:
            mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            mostrar_link(resultado)
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    def on_exportar_excel(e):
        if not reportes_dropdown.value:
            mostrar_mensaje_error(page, "Debe seleccionar un reporte")
            return

        if reportes_dropdown.value == "Productos por Categoria":
            datos = reporte_productos_por_categoria(db)
            encabezados_visibles = ["Categoría", "Total"]
            claves = ["categoria_nombre", "total"]
            resultado = exportar_excel("Productos_por_Categoria.xlsx", encabezados_visibles, claves, datos)

        elif reportes_dropdown.value == "Stock Bajo":
            datos = reporte_stock_bajo(db)
            encabezados_visibles = ["Id", "Nombre", "Cantidad"]
            claves = ["id", "nombre", "cantidad"]
            resultado = exportar_excel("Stock_Bajo.xlsx", encabezados_visibles, claves, datos)

        elif reportes_dropdown.value == "Valor del Inventario":
            datos = reporte_valor_inventario(db)
            encabezados_visibles = ["Id", "Nombre", "Cantidad", "Categoría", "Valor Total"]
            claves = ["id", "nombre", "cantidad", "categoria_nombre", "total"]
            resultado = exportar_excel("Valor_Inventario.xlsx", encabezados_visibles, claves, datos)

        elif reportes_dropdown.value == "Administrativo":
            datos = reporte_administrativo_productos(db)
            encabezados_visibles = ["Id", "Nombre", "Cantidad", "Precio Unitario", "Valor Total",
                                    "Categoría", "Fecha de Creación"]
            claves = ["id", "nombre", "cantidad", "precio", "total", "categoria_nombre", "fecha_creacion"]
            resultado = exportar_excel("Reporte_Administrativo.xlsx", encabezados_visibles, claves, datos)

        if resultado["ok"]:
            mostrar_mensaje(page, resultado["mensaje"], color="#28a745")
            mostrar_link(resultado)
        else:
            mostrar_mensaje_error(page, resultado["mensaje"])

    botones_exportar = ft.Row(
        controls=[
            ft.Button("Exportar CSV", on_click=on_exportar_csv, bgcolor="#0D6EFD", color="WHITE"),
            ft.Button("Exportar Excel", on_click=on_exportar_excel, bgcolor="#198754", color="WHITE"),
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    contenido = ft.Column(
        spacing=20,
        controls=[
            ft.Text("Reportes del Inventario 📊", size=30, color="white"),
            reportes_dropdown,
            botones_exportar,
            link_container
        ],
        expand=True
    )

    contenido_con_fondo = ft.Container(bgcolor="#282728", expand=True, content=contenido)

    return app_layout(
        page,
        contenido_con_fondo,
        selected_index=1
    )
