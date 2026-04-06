from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": "Mi primera API 🚀"}

tareas = ["Estudiar", "Hacer proyecto", "Entrenar"]

@app.get("/tarea")
def obtener_tareas():
    return tareas


@app.post("/tareas")
def crear_tarea(tarea: str):
    tareas.append(tarea)
    return {"mensaje": "Tarea agregada"}