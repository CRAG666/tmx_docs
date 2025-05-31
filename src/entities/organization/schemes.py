from sqlmodel import SQLModel
from typing import TypedDict
from datetime import datetime

# Modelo para exponer datos de Organization (información pública)
class OrganizationPublic(SQLModel):
    id: str
    Name: str
    CreatedAt: datetime


# Modelo para la creación de una organización
class OrganizationCreate(SQLModel):
    Name: str
    IsInternal: bool | None = []
    StateID: str | None = None
    RoleIds: list[str] | None = []


# Modelo para actualizar a una organización
class OrganizationUpdate(SQLModel):
    Name: str
    IsInternal: bool | None = []
    StateID: str | None = None
    RoleIds: list[str] | None = []


class OrganizationUpdateDict(TypedDict):
    Name: str | None
    IsInternal: bool | None
    StateID: str | None
