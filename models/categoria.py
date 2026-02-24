from datetime import datetime
from sqlalchemy import String, Integer, Float, Column, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from database import Base



class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    fecha_creacion = Column(DateTime, nullable=False,
                            default=datetime.utcnow)
    productos = relationship("Producto", back_populates="categoria")

