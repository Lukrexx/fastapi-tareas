from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Usuario
from auth import hash_password,verificar_password,crear_token


router = APIRouter(prefix="/auth", tags=["auth"])
#registro
@router.post("/registro")
def registrar(username: str, password: str):
    db = SessionLocal()

    usuario_existente = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="usuario ya existe")

    nuevo = Usuario(username=username, password=hash_password(password))
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"mensaje": "usuario creado"}

#logueo
@router.post("/login")
def login(username: str, password: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if not usuario or not verificar_password(password, usuario.password):
        raise HTTPException(status_code=400, detail="credenciales incorrectas")

    token = crear_token({"sub": usuario.username})

    return {
        "mensaje": "login exitoso",
        "token": token
    }