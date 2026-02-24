import os
import csv
from openpyxl import Workbook
from sqlalchemy import func
from models import Producto, Categoria

# Carpeta pública para reportes
OUTPUT_DIR = "assets/reports/"

def exportar_excel(nombre_archivo, encabezados_visibles, claves, resultados, hoja="Reporte"):
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(OUTPUT_DIR + nombre_archivo), exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = hoja
    ws.append(encabezados_visibles)

    for r in resultados:
        fila = [r[campo] for campo in claves]
        ws.append(fila)

    wb.save(OUTPUT_DIR + nombre_archivo)
    return {
        "ok": True,
        "mensaje": f"Reporte exportado a {nombre_archivo}",
        "archivo": nombre_archivo
    }

def exportar_csv(nombre_archivo, encabezados_visibles, claves, resultados):
    os.makedirs(os.path.dirname(OUTPUT_DIR + nombre_archivo), exist_ok=True)

    with open(OUTPUT_DIR + nombre_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(encabezados_visibles)
        for r in resultados:
            fila = [r[campo] for campo in claves]
            writer.writerow(fila)

    return {
        "ok": True,
        "mensaje": f"Reporte exportado a {nombre_archivo}",
        "archivo": nombre_archivo
    }

# Reporte: productos por categoría
def reporte_productos_por_categoria(db):
    resultados = (
        db.query(Categoria.id, Categoria.nombre, func.count(Producto.id).label("total"))
        .join(Producto, Producto.categoria_id == Categoria.id)
        .group_by(Categoria.id, Categoria.nombre)
        .all()
    )
    return [{"categoria_id": r[0], "categoria_nombre": r[1], "total": r[2]} for r in resultados]

# Reporte: stock bajo
def reporte_stock_bajo(db):
    resultados = db.query(Producto).filter(Producto.cantidad < 5).all()
    return [{"id": p.id, "nombre": p.nombre, "cantidad": p.cantidad} for p in resultados]

# Reporte: valor del inventario
def reporte_valor_inventario(db):
    resultados = db.query(
        Producto.id,
        Producto.nombre,
        Producto.cantidad,
        (Producto.cantidad * Producto.precio).label("total"),
        Categoria.nombre
    ).join(Categoria, Producto.categoria_id == Categoria.id) \
     .filter(Producto.cantidad > 0).all()

    return [{"id": r[0], "nombre": r[1], "cantidad": r[2], "total": r[3], "categoria_nombre": r[4]} for r in resultados]

# Reporte: administrativo de productos
def reporte_administrativo_productos(db):
    resultados = db.query(
        Producto.id,
        Producto.nombre,
        Producto.cantidad,
        Producto.precio,
        (Producto.cantidad * Producto.precio).label("total"),
        Categoria.nombre,
        Producto.fecha_creacion
    ).join(Categoria, Producto.categoria_id == Categoria.id) \
     .order_by((Producto.cantidad * Producto.precio).asc()).all()

    return [
        {
            "id": r[0],
            "nombre": r[1],
            "cantidad": r[2],
            "precio": r[3],
            "total": r[4],
            "categoria_nombre": r[5],
            "fecha_creacion": r[6]
        }
        for r in resultados
    ]