from fastapi import FastAPI, Header, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

security = HTTPBearer()

SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"

# Base de datos
DATABASE_URL = "sqlite:///./tareas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#clase
class TareaCreate(BaseModel):
    nombre: str

#usuarios 
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)

#token 
def crear_token(data: dict):
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=30)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

#funcion verificar token
def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

#registro
@app.post("/registro")
def registrar(username: str, password: str):
    db = SessionLocal()

    usuario_existente = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario_existente:
        return {"error": "usuario ya existe"}

    nuevo = Usuario(username=username, password=password)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {"mensaje": "usuario creado"}

#logueo
@app.post("/login")
def login(username: str, password: str):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.username == username).first()

    if not usuario or usuario.password != password:
        return {"error": "credenciales incorrectas"}

    token = crear_token({"sub": usuario.username})

    return {
        "mensaje": "login exitoso",
        "token": token
    }

# Modelo
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

Base.metadata.create_all(bind=engine)

# Crear tarea
@app.post("/tareas")
def crear_tarea(tarea: TareaCreate):
    db = SessionLocal()
    nueva = Tarea(nombre=tarea.nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Obtener tareas
@app.get("/tareas")
def obtener_tareas(user=Depends(verificar_token)):
    db = SessionLocal()
    return db.query(Tarea).all()

#eliminar tareas
@app.delete("/tareas/{id}")
def eliminar_tarea(id: int):
    db = SessionLocal()
    tarea = db.query(Tarea).filter(Tarea.id == id).first()

    if tarea:
        db.delete(tarea)
        db.commit()
        return {"mensaje": "Tarea eliminada"}
    
    return {"error": "No encontrada"}

#editar tareas 
@app.put("/tareas/{id}")
def actualizar_tarea(id: int, tarea: TareaCreate):
    db = SessionLocal()
    tarea = db.query(Tarea).filter(Tarea.id == id).first()

    if tarea:
        tarea.nombre = tarea.nombre
        db.commit()
        return {"mensaje": "Actualizada"}
    
    return {"error": "No encontrada"}