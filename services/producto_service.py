from sqlalchemy.orm import Session
from models import Categoria
from models.producto import Producto


def crear_producto(db: Session, datos: dict):
    id_producto = datos.get("id")
    nombre = datos.get("nombre", "").strip()
    precio = datos.get("precio")
    cantidad = datos.get("cantidad")
    categoria_id = datos.get("categoria_id")

    if id_producto is None or id_producto <= 0:
        return {"ok": False, "mensaje": "El id es obligatorio y debe ser mayor a 0"}

    if not nombre:
        return {"ok": False, "mensaje": "El nombre del producto es obligatorio"}

    if precio is None or precio <= 0:
        return {"ok": False, "mensaje": "El precio debe ser mayor a 0"}

    if cantidad is None or cantidad <= 0:
        return {"ok": False, "mensaje": "La cantidad debe ser mayor a 0"}

    if categoria_id is None or categoria_id <= 0:
        return {"ok": False, "mensaje": "El id de categoría es obligatorio y debe ser mayor que 0"}

    existente = db.query(Producto).filter(Producto.id == id_producto).first()
    if existente:
        return {"ok": False, "mensaje": "El id del producto ya existe"}

    categoria_existente = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_existente:
        return {"ok": False, "mensaje": "La categoría indicada no existe"}

    nuevo_producto = Producto(
        id=id_producto,
        nombre=nombre,
        precio=precio,
        cantidad=cantidad,
        categoria_id=categoria_id,
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {
        "ok": True,
        "mensaje": "Producto creado con éxito",
        "producto": {
            "id": nuevo_producto.id,
            "nombre": nuevo_producto.nombre,
            "precio": nuevo_producto.precio,
            "cantidad": nuevo_producto.cantidad,
            "categoria_id": nuevo_producto.categoria_id,
        },
    }


def consulta_id_producto(db: Session, producto_id: int):
    if producto_id is None or producto_id <= 0:
        return {"ok": False, "mensaje": "El id es obligatorio y debe ser mayor a 0"}

    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto is None:
        return {"ok": False, "mensaje": "El producto no existe"}

    return {
        "ok": True,
        "mensaje": "Producto encontrado",
        "producto": {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad,
            "categoria_id": producto.categoria_id,
        },
    }


def listado_productos(db: Session):
    productos = db.query(Producto).order_by(Producto.id).all()
    if not productos:
        return {"ok": False, "mensaje": "No existen productos"}

    lista = [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "cantidad": p.cantidad,
            "categoria_id": p.categoria_id,
        }
        for p in productos
    ]

    return {"ok": True, "mensaje": "Productos existentes", "productos": lista}


def actualizar_producto(db: Session, producto_id: int, nombre: str, precio: float, cantidad: int, categoria_id: int):
    if producto_id is None or producto_id <= 0:
        return {"ok": False, "mensaje": "El id es obligatorio y debe ser mayor a 0"}

    if not nombre:
        return {"ok": False, "mensaje": "El nombre del producto es obligatorio"}

    if precio is None or precio <= 0:
        return {"ok": False, "mensaje": "El precio debe ser mayor a 0"}

    if cantidad is None or cantidad < 0:
        return {"ok": False, "mensaje": "La cantidad debe ser mayor o igual a 0"}

    if categoria_id is None or categoria_id <= 0:
        return {"ok": False, "mensaje": "El id de categoría es obligatorio y debe ser mayor que 0"}

    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return {"ok": False, "mensaje": "El producto no existe"}

    producto.nombre = nombre
    producto.precio = precio
    producto.cantidad = cantidad
    producto.categoria_id = categoria_id

    db.commit()
    db.refresh(producto)

    return {
        "ok": True,
        "mensaje": "Producto actualizado con éxito",
        "producto": {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "cantidad": producto.cantidad,
            "categoria_id": producto.categoria_id,
        },
    }


def eliminar_producto(db: Session, producto_id: int):
    if producto_id is None or producto_id <= 0:
        return {"ok": False, "mensaje": "El id es obligatorio y debe ser mayor a 0"}

    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return {"ok": False, "mensaje": "No existe el producto"}

    nombre = producto.nombre
    db.delete(producto)
    db.commit()

    return {"ok": True, "mensaje": f"Producto {nombre} eliminado con éxito"}