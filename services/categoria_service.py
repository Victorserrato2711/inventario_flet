from models.categoria import Categoria
from sqlalchemy.orm import Session


def crear_categoria(db: Session, categoria_id: int, nombre: str):
    try:
        categoria_id = int(categoria_id)
    except (ValueError, TypeError):
        return {"ok": False, "mensaje": "El id debe ser un número válido"}

    if categoria_id <= 0:
        return {"ok": False, "mensaje": "El id no puede ser menor o igual que 0"}

    nombre = nombre.strip()
    if not nombre:
        return {"ok": False, "mensaje": "El nombre es obligatorio"}

    # Validar duplicados por id
    existente_id = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if existente_id:
        return {"ok": False, "mensaje": "Ya existe una categoría con ese id"}

    # Validar duplicados por nombre
    existente_nombre = db.query(Categoria).filter(Categoria.nombre.ilike(nombre)).first()
    if existente_nombre:
        return {"ok": False, "mensaje": "Ya existe una categoría con ese nombre"}

    nueva = Categoria(id=categoria_id, nombre=nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return {"ok": True, "mensaje": "Categoría creada con éxito", "id": nueva.id}


def consulta_id_categoria(db: Session, categoria_id: int):
    if categoria_id is None:
        return {"ok": False, "mensaje": "El id es obligatorio"}

    if categoria_id <= 0:
        return {"ok": False, "mensaje": "El id no puede ser menor que 0"}

    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()

    if categoria is None:
        return {"ok": False, "mensaje": "La Categoria No Existe"}

    return {
        "ok": True,
        "mensaje": "Categoria encontrada",
        "categoria": {
            "id": categoria.id,
            "nombre": categoria.nombre
        }
    }


def listado_categorias(db: Session):
    categorias = db.query(Categoria).order_by(Categoria.id).all()

    if not categorias:
        return {"ok": False, "mensaje": "No Existen Categorias"}

    lista = [{"id": c.id, "nombre": c.nombre} for c in categorias]

    return {"ok": True, "mensaje": "Categorias existentes", "categorias": lista}


def actualizar_categoria(db: Session, categoria_id: int, nombre: str):
    if categoria_id is None:
        return {"ok": False, "mensaje": "El id es obligatorio"}

    try:
        categoria_id = int(categoria_id)
    except ValueError:
        return {"ok": False, "mensaje": "El id debe ser un número válido"}

    if categoria_id <= 0:
        return {"ok": False, "mensaje": "El id no puede ser menor o igual que 0"}

    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        return {"ok": False, "mensaje": "No existe la categoría"}

    nombre = nombre.strip()
    if not nombre:
        return {"ok": False, "mensaje": "El nombre es obligatorio"}

    if nombre.lower() == categoria.nombre.lower():
        return {"ok": False, "mensaje": "El nombre es igual al actual, no se realizaron cambios"}

    existente = db.query(Categoria).filter(
        Categoria.nombre == nombre,
        Categoria.id != categoria_id
    ).first()
    if existente:
        return {"ok": False, "mensaje": "Ya existe una categoría con ese nombre"}

    categoria.nombre = nombre
    db.commit()
    db.refresh(categoria)

    return {"ok": True, "mensaje": "Categoría actualizada con éxito"}


def eliminar_categoria(db: Session, categoria_id: int):
    if categoria_id is None:
        return {"ok": False, "mensaje": "El id es obligatorio"}

    try:
        categoria_id = int(categoria_id)
    except (ValueError, TypeError):
        return {"ok": False, "mensaje": "El id debe ser un número válido"}

    if categoria_id <= 0:
        return {"ok": False, "mensaje": "El id no puede ser menor o igual que 0"}

    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        return {"ok": False, "mensaje": "No existe la categoría"}

    db.delete(categoria)
    db.commit()

    return {"ok": True, "mensaje": f"Categoría con id {categoria_id} eliminada con éxito"}