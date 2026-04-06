from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI()

# Base de datos
DATABASE_URL = "sqlite:///./tareas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

Base.metadata.create_all(bind=engine)

# Crear tarea
@app.post("/tareas")
def crear_tarea(nombre: str):
    db = SessionLocal()
    nueva = Tarea(nombre=nombre)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Obtener tareas
@app.get("/tareas")
def obtener_tareas():
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
def actualizar_tarea(id: int, nombre: str):
    db = SessionLocal()
    tarea = db.query(Tarea).filter(Tarea.id == id).first()

    if tarea:
        tarea.nombre = nombre
        db.commit()
        return {"mensaje": "Actualizada"}
    
    return {"error": "No encontrada"}