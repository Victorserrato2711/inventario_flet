from datetime import datetime
from sqlalchemy import String, Integer, Column, DateTime, ForeignKey, Numeric, VARCHAR
from sqlalchemy.orm import relationship
from database import Base

class Entradas(Base):
    __tablename__ = "entradas"

    id_entrada = Column(VARCHAR, primary_key=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario_nombre = Column(String(100), nullable=False)
    fecha_registro = Column(DateTime, nullable=False, default=datetime.now())
    total_productos = Column(Integer, nullable=False)
    total_unidades = Column(Numeric(10,3), nullable=False)

    usuario = relationship("Usuario", back_populates="entradas")
    detalles = relationship("DetalleEntradas",back_populates="entrada")

class DetalleEntradas(Base):
    __tablename__ = "detalle_entradas"

    id = Column(Integer, primary_key=True, nullable=False)
    id_entrada = Column(VARCHAR, ForeignKey("entradas.id_entrada"),nullable=False)
    producto_id = Column(Integer,ForeignKey("productos.id"),nullable=False)
    nombre_producto = Column(String(100),nullable=False)
    cantidad = Column(Numeric(10,3),nullable=False)

    producto = relationship("Producto", back_populates="detalle_entradas")
    entrada = relationship("Entradas",back_populates="detalles")