from fastapi import FastAPI
from routes.tareas import router as tareas_router
from routes.usuarios import router as usuarios_router

app = FastAPI()

app.include_router(usuarios_router)
app.include_router(tareas_router)