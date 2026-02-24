from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Venta(Base):
    __tablename__ = "ventas"

    id_venta = Column(String(6), primary_key=True, unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    fecha = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    metodo_pago = Column(String(20), nullable=False)

    # Relación con Usuario y Detalles
    usuario = relationship("Usuario")  # acceso directo al objeto Usuario
    detalles = relationship("DetalleVenta", back_populates="venta")


class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(String(6), ForeignKey("ventas.id_venta"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    nombre_producto = Column(String(100), nullable=False)
    cantidad = Column(Float, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    # Relación con Venta
    venta = relationship("Venta", back_populates="detalles")