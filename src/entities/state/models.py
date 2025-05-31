from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from src.config.base.utils import get_uuid


# Tabla de estados
class State(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True)
    descripcion: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Relaciones inversas
    # organizations: list["Organization"] = Relationship(back_populates="state")
    # users: list["User"] = Relationship(back_populates="state")
    devices: list["Device"] = Relationship(back_populates="state")


class StateHistory(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    entity_type: str = Field(max_length=50)  # Ej: "User", "Device", "Organization"
    entity_id: str  # ID de la entidad correspondiente
    previous_state_id: str | None = Field(foreign_key="state.id")
    state_id: str = Field(foreign_key="state.id")
    changed_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    previous_state: Optional[State] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[StateHistory.previous_state_id]"}
    )
    current_state: State = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[StateHistory.state_id]"}
    )
