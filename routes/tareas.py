from fastapi import APIRouter, Depends, HTTPException
from schemas import TareaCreate
from auth import verificar_token
from database import SessionLocal
from models import Tarea

router = APIRouter(prefix="/tareas", tags=["tareas"])

# Obtener tareas
@router.get("/tareas")
def obtener_tareas(user=Depends(verificar_token)):
    db = SessionLocal()
    username = user["sub"]  # viene del token
    return db.query(Tarea).filter(Tarea.usuario == username).all()

# Crear tarea
@router.post("/tareas")
def crear_tarea(tarea: TareaCreate, user=Depends(verificar_token)):
    db = SessionLocal()
    username = user["sub"]
    nueva = Tarea(
        nombre=tarea.nombre,
        usuario=username  # clave
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva

#eliminar tareas
@router.delete("/tareas/{id}")
def eliminar_tarea(id: int, user=Depends(verificar_token)):
    db = SessionLocal()
    username = user["sub"]

    tarea_db = db.query(Tarea).filter(Tarea.id == id, Tarea.usuario == username).first()

    if tarea_db:
        db.delete(tarea_db)
        db.commit()
        return {"mensaje": "Tarea eliminada"}
    
    raise HTTPException(status_code=400, detail="No encontrada")

#editar tareas 
@router.put("/tareas/{id}")
def actualizar_tarea(id: int, nueva_tarea: TareaCreate, user=Depends(verificar_token)):
    db = SessionLocal()
    username = user["sub"]

    tarea = db.query(Tarea).filter(Tarea.id == id, Tarea.usuario == username).first()

    if tarea:
        tarea.nombre = nueva_tarea.nombre
        db.commit()
        return {"mensaje": "Actualizada"}
    
    raise HTTPException(status_code=400, detail="No encontrada")