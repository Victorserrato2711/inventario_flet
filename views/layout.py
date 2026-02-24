import flet as ft
from services.salir_service import logout_usuario

def app_layout(page: ft.Page, contenido, selected_index=0, route="/home"):
    async def handle_nav(e):
        index = e.control.selected_index
        if index == 0:
            await page.push_route("/home")
        elif index == 1:
            await page.push_route("/reportes")
        elif index == 2:
            await page.push_route("/usuarios")
        elif index == 3:
            await page.push_route("/cambiar_contraseña")
        elif index == 4:
            await page.push_route("/pos")
        elif index == 5:
            await page.push_route("/entradas")
        elif index == 6:
            await page.push_route("/logout")

    return ft.View(
        route=route,
        expand=True,
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    ft.NavigationRail(
                        selected_index=selected_index,
                        destinations=[
                            ft.NavigationRailDestination(icon=ft.Icons.INVENTORY, label="Home"),
                            ft.NavigationRailDestination(icon=ft.Icons.ANALYTICS, label="Reportes"),
                            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Usuarios"),
                            ft.NavigationRailDestination(icon=ft.Icons.KEY, label="Cambio de Contraseña"),
                            ft.NavigationRailDestination(icon=ft.Icons.POINT_OF_SALE, label="POS"),
                            ft.NavigationRailDestination(icon=ft.Icons.WAREHOUSE, label = "Entradas"),
                            ft.NavigationRailDestination(icon=ft.Icons.LOGOUT, label="Cerrar Sesión"),
                        ],
                        on_change=handle_nav,
                        expand=False,
                        extended=False,
                        min_width=72,
                        group_alignment=-0.9
                    ),
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        expand=True,
                        content=contenido
                    ),
                ],
            )
        ],
    )