from datetime import datetime
import random
from sqlalchemy import text

def registrar_entrada(db, usuario_id, productos):
    try:
        result = db.execute(
            text("SELECT nombre FROM usuarios WHERE id = :usuario_id"),
            {"usuario_id": usuario_id}
        ).fetchone()

        if not result:
            raise ValueError("Usuario no existe")

        usuario_nombre = result[0]
        id_entrada = str(random.randint(0, 999999)).zfill(6)
        total_productos = len(productos)
        total_unidades = sum([p["cantidad"] for p in productos])

        db.execute(
            text("""
                INSERT INTO entradas (id_entrada, usuario_id, usuario_nombre, fecha_registro, total_productos, total_unidades)
                VALUES (:id_entrada, :usuario_id, :usuario_nombre, :fecha_registro, :total_productos, :total_unidades)
            """),
            {
                "id_entrada": id_entrada,
                "usuario_id": usuario_id,
                "usuario_nombre": usuario_nombre,
                "fecha_registro": datetime.now(),
                "total_productos": total_productos,
                "total_unidades": total_unidades
            }
        )
        for p in productos:
            if not p.get("producto_id") or not p.get("cantidad"):
                raise ValueError("Producto inválido: campos vacíos")
            if p["cantidad"] <= 0:
                raise ValueError("Cantidad debe ser mayor a 0")

            result_prod = db.execute(
                text("SELECT nombre FROM productos WHERE id = :producto_id"),
                {"producto_id": p["producto_id"]}
            ).fetchone()

            if not result_prod:
                raise ValueError(f"Producto con ID {p['producto_id']} no existe")

            nombre_producto = result_prod[0]

            db.execute(
                text("""
                    INSERT INTO detalle_entradas (id_entrada, producto_id, nombre_producto, cantidad)
                    VALUES (:id_entrada, :producto_id, :nombre_producto, :cantidad)
                """),
                {
                    "id_entrada": id_entrada,
                    "producto_id": p["producto_id"],
                    "nombre_producto": nombre_producto,
                    "cantidad": p["cantidad"]
                }
            )

            db.execute(
                text("""
                    UPDATE productos
                    SET cantidad = cantidad + :cantidad
                    WHERE id = :producto_id
                """),
                {
                    "cantidad": p["cantidad"],
                    "producto_id": p["producto_id"]
                }
            )
        db.commit()

        return {
            "ok": True,
            "mensaje": f"Entrada registrada con ID {id_entrada}",
            "id_entrada": id_entrada
        }

    except Exception as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al registrar entrada: {e}"}