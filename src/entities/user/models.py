from sqlmodel import SQLModel, Field, Relationship
from src.config.base.utils import get_uuid


# Tabla de enlace para relación muchos-a-muchos entre User y UserRole
class UserRoleUserLink(SQLModel, table=True):
    user_id: str = Field(foreign_key="user.id", primary_key=True)
    role_id: str = Field(foreign_key="userrole.id", primary_key=True)


# Modelo UserRole (Roles únicos)
class UserRole(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    name: str = Field(unique=True, index=True)
    # Relación inversa: usuarios que tienen este rol
    users: list["User"] = Relationship(
        back_populates="roles",
        link_model=UserRoleUserLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# Modelo UserIdentity (Credenciales únicas por usuario)
class UserIdentity(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str = Field(index=True)
    user_id: str = Field(foreign_key="user.id")
    # Relación inversa con User
    user: "User" = Relationship(
        back_populates="identity",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


# Modelo User (Datos principales del usuario)
class User(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    Name: str = Field(index=True)
    LastName: str = Field(index=True)
    Email: str = Field(unique=True, index=True)
    Tel: str = Field(unique=True, index=True)
    # Relación 1:1 con UserIdentity
    identity: UserIdentity | None = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    # Relación muchos-a-muchos con UserRole
    roles: list[UserRole] = Relationship(
        back_populates="users",
        link_model=UserRoleUserLink,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    @property
    def username(self):
        if self.identity:
            return self.identity.username
        return None
