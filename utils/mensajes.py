import flet as ft
import asyncio

# --- mensaje de éxito ---
def mostrar_mensaje(page: ft.Page, mensaje: str, color="#28a745"):
    aviso = ft.Container(
        bgcolor=color,
        padding=20,
        margin=10,
        border_radius=10,
        content=ft.Text(mensaje, color="WHITE", size=16, weight="bold"),
        left=page.width / 2 - 150,
        bottom=20,
    )
    page.overlay.append(aviso)
    page.update()

    async def cerrar():
        await asyncio.sleep(5)
        page.overlay.remove(aviso)
        page.update()
    asyncio.create_task(cerrar())



# --- mensaje de error ---
def mostrar_mensaje_error(page: ft.Page, mensaje: str):
    aviso = ft.Row(
        controls=[
            ft.Container(
                bgcolor=ft.Colors.RED_400,
                padding=20,
                margin=10,
                border_radius=10,
                content=ft.Text(mensaje, color="WHITE", size=16, weight="bold"),
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    page.overlay.append(aviso)
    page.update()

    async def cerrar():
        await asyncio.sleep(3)
        page.overlay.remove(aviso)
        page.update()
    asyncio.create_task(cerrar())

