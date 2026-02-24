import secrets
from datetime import datetime

import bcrypt
from oauthlib.uri_validate import query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario


# ---- Habilitar Usuario -----
def habilitar_usuario(db: Session, usuario_id: int):
    try:
        usuario = db.query(Usuario).filter_by(id=usuario_id).first()
        if usuario:
            usuario.activo = True
            db.commit()
            db.refresh(usuario)
            return {"ok": True, "mensaje": "Usuario habilitado correctamente", "usuario": usuario.to_dict()}
        return {"ok": False, "mensaje": "Usuario no encontrado"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al habilitar usuario: {str(e)}"}


# ---- Login ----
def login_usuario(db: Session, usuario: str, contraseña: str):
    try:
        usuario_obj = db.query(Usuario).filter(Usuario.usuario == usuario.strip()).first()
        if not usuario_obj:
            return {"ok": False, "mensaje": "Usuario no encontrado"}

        if not usuario_obj.activo:
            return {"ok": False, "mensaje": "Usuario deshabilitado"}

        if not bcrypt.checkpw(contraseña.encode("utf-8"),
                              usuario_obj.contrasena.encode("utf-8")):
            return {"ok": False, "mensaje": "Contraseña incorrecta"}

        if usuario_obj.requiere_cambio:
            return {
                "ok": True,
                "mensaje": "Debe actualizar su contraseña",
                "requiere_cambio": True,
                "usuario": usuario_obj.to_dict()
            }
        with open("turno_actual.txt", "w") as f:
            f.write(f"{usuario_obj.id},{0},{datetime.now()}\n")

        return {
            "ok": True,
            "mensaje": "Login exitoso",
            "requiere_cambio": False,
            "usuario": usuario_obj.to_dict()
        }

    except SQLAlchemyError as e:
        return {"ok": False, "mensaje": f"Error en login: {str(e)}"}

# --- Cambio de Contraseña ---
def cambiar_contraseña(db: Session, usuario: str, nueva_contraseña: str):
    try:
        usuario_obj = db.query(Usuario).filter(Usuario.usuario == usuario.strip()).first()
        if not usuario_obj:
            return {"ok": False, "mensaje": "Usuario no encontrado"}

        # Generar hash temporal (el usuario deberá cambiarla en login)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(nueva_contraseña.encode("utf-8"), salt).decode("utf-8")
        usuario_obj.contrasena = hashed

        usuario_obj.requiere_cambio = True

        db.commit()
        return {"ok": True, "mensaje": "Contraseña temporal asignada"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al actualizar contraseña: {str(e)}"}


# ---- Crear Usuario ---
def crear_usuario(db: Session, usuario: str, nombre: str, correo: str, puesto: str):
    try:
        # Normalización de entradas
        usuario = usuario.strip() if usuario else None
        nombre = nombre.strip() if nombre else None
        puesto = puesto.strip() if puesto else None
        correo = correo.strip() if correo else None

        # Validaciones básicas
        if not usuario or not nombre or not puesto:
            return {"ok": False, "mensaje": "Usuario, nombre y puesto son obligatorios"}

        if correo and "@" not in correo:
            return {"ok": False, "mensaje": "Correo inválido"}

        existente = db.query(Usuario).filter(Usuario.usuario == usuario).first()
        if existente:
            return {"ok": False, "mensaje": "El usuario ya existe"}

        if correo:
            existente_correo = db.query(Usuario).filter(Usuario.correo == correo).first()
            if existente_correo:
                return {"ok": False, "mensaje": "El correo ya está registrado"}

        # Generar contraseña temporal
        temp_pass = secrets.token_hex(4)
        hashed = bcrypt.hashpw(temp_pass.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        nuevo = Usuario(
            usuario=usuario,
            nombre=nombre,
            correo=correo if correo else None,
            puesto=puesto,
            contrasena=hashed,
            requiere_cambio=True,
            activo=True
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        return {
            "ok": True,
            "mensaje": "Usuario creado correctamente",
            "usuario": nuevo.to_dict(),
            "contrasena_temporal": temp_pass
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al crear usuario: {str(e)}"}


# ---- Editar Usuario ----
def editar_usuario(db: Session, usuario_id: int, nombre: str = None,
                   correo: str = None, puesto: str = None, activo: bool = None):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return {"ok": False, "mensaje": "Usuario no encontrado"}

        if nombre is not None:
            usuario.nombre = nombre.strip()
        if correo is not None:
            usuario.correo = correo.strip()
        if puesto is not None:
            usuario.puesto = puesto.strip()
        if activo is not None:
            usuario.activo = activo

        db.commit()
        db.refresh(usuario)

        return {"ok": True, "mensaje": "Usuario actualizado correctamente", "usuario": usuario.to_dict()}
    except SQLAlchemyError as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al editar usuario: {str(e)}"}


# ---- Deshabilitar Usuario ----
def deshabilitar_usuario(db: Session, usuario_id: int):
    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return {"ok": False, "mensaje": "Usuario no encontrado"}

        usuario.activo = False
        db.commit()
        db.refresh(usuario)

        return {"ok": True, "mensaje": "Usuario deshabilitado correctamente", "usuario": usuario.to_dict()}
    except SQLAlchemyError as e:
        db.rollback()
        return {"ok": False, "mensaje": f"Error al deshabilitar usuario: {str(e)}"}


# ---- Listar Usuarios ----
def listar_usuarios(db: Session):
    try:
        usuarios = db.query(Usuario).order_by(Usuario.id).all()
        return {"ok": True, "usuarios": [u.to_dict() for u in usuarios]}
    except SQLAlchemyError as e:
        return {"ok": False, "mensaje": f"Error al listar usuarios: {str(e)}"}