from sqlmodel import SQLModel
from typing import TypedDict


# Modelo para exponer datos de UserRole
class UserRolePublic(SQLModel):
    id: str
    Name: str


# Modelo para exponer datos del User (información pública)
class UserPublic(SQLModel):
    id: str
    Name: str
    LastName: str
    UserName: str | None = None
    Roles: list[UserRolePublic] = []


# Modelo para la creación de un usuario
class UserCreate(SQLModel):
    Name: str
    LastName: str
    Email: str
    Tel: str
    UserName: str
    Password: str
    RoleIds: list[str] | None = []


# Modelo para actualizar parcialmente un usuario
class UserUpdate(SQLModel):
    Name: str | None = None
    LastName: str | None = None
    Email: str | None = None
    Tel: str | None = None
    UserName: str | None = None
    Password: str | None = None
    RoleIds: list[str] | None = None


class UserUpdateDict(TypedDict):
    Name: str | None
    LastName: str | None
    Email: str | None
    Tel: str | None
    UserName: str | None
    Password: str | None
    RoleIds: list[str] | None
