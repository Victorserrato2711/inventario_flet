import random
from datetime import datetime
from sqlalchemy import text

from models import Usuario
from models.producto import Producto
from models.venta import Venta, DetalleVenta

def generar_ticket_corte(db, usuario_id):
    resultado = corte_cierre(db, usuario_id)

    if not resultado["ok"]:
        return "Error al Generar Corte"

    ticket = []
    ticket.append("--- Cierre de Caja ---")
    ticket.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    ticket.append(f"Usuario: {usuario_id}")
    ticket.append("------------------------------------------------------")
    ticket.append(f"Fondo Inicial: ${resultado['fondo']:.2f}")
    ticket.append(f"Subtotal Ventas: ${resultado['subtotal']:.2f}")
    ticket.append(f"Retiros: ${resultado['retiros']:.2f}")
    ticket.append("------------------------------------------------------")
    ticket.append(f"Total de Efectivo: ${resultado['efectivo']:.2f}")
    ticket.append(f"Total de Tarjeta: ${resultado['tarjeta']:.2f}")
    ticket.append(f"Total Corte: ${resultado['total']:.2f}")
    ticket.append("=======================================================")

    return "\n".join(ticket)


def corte_cierre(db, usuario_id):
    try:
        with open("turno_actual.txt", "r") as f:
            datos = f.read().split(",")
            fondo_inicial = float(datos[1])
            inicio_turno = datetime.fromisoformat(datos[2].strip())

        ventas = db.query(Venta).filter(
            Venta.usuario_id == usuario_id,
            Venta.fecha >= inicio_turno
        ).all()
        subtotal = sum(v.total for v in ventas)

        retiros_total = 0.0
        with open("retiros.txt", "r") as f:
            for linea in f:
                datos = linea.strip().split(",")
                if int(datos[0]) == usuario_id:
                    retiros_total += float(datos[1])

        total_efectivo = sum(v.total for v in ventas if "Efectivo" in v.metodo_pago)
        total_tarjeta = sum(v.total for v in ventas if "Tarjeta" in v.metodo_pago)

        total_corte = (fondo_inicial + subtotal) - retiros_total

        return {
            "ok": True,
            "fondo": fondo_inicial,
            "subtotal": subtotal,
            "retiros": retiros_total,
            "total": total_corte,
            "efectivo": total_efectivo,
            "tarjeta": total_tarjeta,
            "mensaje": "Corte Generado Correctamente"
        }
    except Exception as e:
        return {"ok": False, "mensaje": f"Error al Generar Corte: {str(e)}"}

def retiro_caja(usuario_id, monto, motivo):
    try:
        with open("retiros.txt", "a") as f:
            f.write(f"{usuario_id},{monto},{motivo},{datetime.now()}\n")
        return {"ok": True, "mensaje": f"Retiro Registrado: ${monto:.2f} por {motivo}"}
    except Exception as e:
        return {"ok": False, "mensaje": f"Error al registrar retiro {e}"}

def iniciar_turno(usuario_id, fondo_inicial):
    try:
        with open("turno_actual.txt", "w") as f:
            f.write(f"{usuario_id},{fondo_inicial},{datetime.now()}\n")
        return {"ok": True, "mensaje": f"Turno iniciado con Fondo ${fondo_inicial:.2f}"}
    except Exception as e:
        return {"ok": False, "mensaje": f"Error al Iniciar turno:{str(e)}"}

def generar_id_venta(db):
    id_venta = str(random.randint(100000, 999999))
    while db.query(Venta).filter_by(id_venta=id_venta).first():
        id_venta = str(random.randint(100000, 999999))
    return id_venta

def buscar_producto(db, codigo):
    producto = db.query(Producto).filter(Producto.id == codigo).first()
    if producto:
        return {
            "ok": True,
            "producto": {
                "id": producto.id,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "cantidad": producto.cantidad
            }
        }
    return {"ok": False, "mensaje": "Producto No encontrado"}

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
        return {"ok": False, "mensaje": f"Error al registrar venta: {e}"}


def registrar_detalle_venta(db, venta_id, producto_id, cantidad, precio_unitario):
    try:
        db.execute(
            text("""
                INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                VALUES (:venta_id, :producto_id, :cantidad, :precio_unitario, :subtotal)
            """),
            {
                "venta_id": venta_id,
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "subtotal": cantidad * precio_unitario
            }
        )
        db.commit()
        return {"ok": True, "mensaje": "Detalle registrado"}
    except Exception as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al registrar detalle: {e}"}



def generar_ticket(id_venta, db, total=0.0, metodo_pago="", monto_entregado=None, cambio=None):
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    detalles = db.query(DetalleVenta).filter(DetalleVenta.id_venta == id_venta).all()
    usuario = db.query(Usuario).filter(Usuario.id == venta.usuario_id).first()
    nombre_usuario = usuario.nombre if usuario else f"Usuario {venta.usuario_id}"

    ticket = []
    ticket.append("---- Ticket de Venta ----")
    ticket.append(f"Id de la Venta: {venta.id_venta}")
    ticket.append(f"Fecha: {venta.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    ticket.append(f"Le Atendió: {nombre_usuario}")   # 🔹 nombre real del usuario
    ticket.append("------------------------------------------------------")

    for d in detalles:
        subtotal = float(d.cantidad) * float(d.precio_unitario)
        ticket.append(
            f"{d.nombre_producto} x{float(d.cantidad):.2f} Sub: ${subtotal:.2f}"
        )

    ticket.append("------------------------------------------------------")
    ticket.append(f"Total Venta: ${float(total):.2f}")
    ticket.append(f"Método de Pago: {metodo_pago}")

    if monto_entregado is not None:
        ticket.append(f"Monto Entregado: ${float(monto_entregado):.2f}")
    if cambio is not None:
        ticket.append(f"Cambio: ${float(cambio):.2f}")

    ticket.append("=======================================================")
    ticket.append("¡¡Gracias por su Visita, Vuelva Pronto!!")

    return "\n".join(ticket)

