from database import Base, engine
from sqlalchemy import Column, Integer, String

#usuarios 
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
#Tarea
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    usuario = Column(String)

Base.metadata.create_all(bind=engine)