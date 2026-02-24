from datetime import datetime
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base   # <-- Importar Base desde database.py

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, index=True)
    precio = Column(Numeric(10, 2), nullable=False)
    cantidad = Column(Integer, nullable=False)
    categoria_id = Column(ForeignKey("categorias.id"), index=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="productos")

    detalle_entradas = relationship("DetalleEntradas", back_populates="producto")

