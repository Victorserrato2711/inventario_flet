from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id= Column(Integer,primary_key=True, autoincrement=True)
    usuario= Column(String(10), nullable=False, unique=True)
    nombre= Column(String(150),nullable=False)
    puesto= Column(String(50),nullable=False,default="empleado")
    activo= Column(Boolean,default=True)
    correo= Column(String,nullable=True)
    contrasena= Column(String(200),nullable=False)
    requiere_cambio = Column(Boolean, default=True)

    def to_dict(self):
        return{
            "id":self.id,
            "usuario":self.usuario,
            "nombre":self.nombre,
            "puesto":self.puesto,
            "activo":self.activo,
            "correo":self.correo,
            "contrasena":self.contrasena,
            "requiere_cambio":self.requiere_cambio
        }

    entradas = relationship("Entradas", back_populates="usuario")
