import bcrypt

# Contraseña que quieres probar
password_ingresada = "Pruebas123"

# Hash guardado en la BD
hash_guardado = "$2b$12$FRlE3zg4rCXgcqtfwUL9Qu11kM09TTbjUyHfwH/BFUON13L6wZetm"

# Verificar si coincide
if bcrypt.checkpw(password_ingresada.encode("utf-8"), hash_guardado.encode("utf-8")):
    print("✅ La contraseña coincide con la guardada en la BD")
else:
    print("❌ La contraseña NO coincide")


    def quitar_confirmacion(e=None):
        nonlocal confirmacion
        if confirmacion in page.controls:
            page.controls.remove(confirmacion)
            page.update()



def mostrar_opciones_pago(e):
    nonlocal confirmacion
    if not productos:
        mostrar_mensaje_error(page, "No hay productos a la venta")
        return

    pago_efectivo_input.value = "0"
    pago_tarjeta_input.value = "0"

    confirmacion = ft.Container(
        bgcolor=ft.Colors.BLACK,
        padding=20,
        alignment=ft.alignment.Alignment(1, 0),   # derecha, centrado vertical
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

    # 🔹 Agregar al overlay en lugar del layout normal
    page.overlay.append(confirmacion)
    page.update()
