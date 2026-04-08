from pydantic import BaseModel

#clase
class TareaCreate(BaseModel):
    nombre: str