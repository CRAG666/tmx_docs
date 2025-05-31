from sqlmodel import SQLModel


#Esquema para exponer los registros de la tabla State
class StatePublic(SQLModel):
    id: str
    nombre: str
    descripcion: str | None

