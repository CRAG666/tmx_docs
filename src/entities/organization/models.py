from sqlmodel import SQLModel, Field, Relationship
from config.base.utils import get_uuid


# Modelo OrganizationIdentity
class OrganizationIdentity(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    organization: str = Field(unique=True, index=True)
    organization_id: str = Field(foreign_key="organization.id")
    # organization: "Organization" = Relationship(
    #     back_populates="identity",
    #     sa_relationship_kwargs={"lazy": "selectin"},
    # )


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
