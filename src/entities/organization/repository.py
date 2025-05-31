from sqlmodel import Session, select
from fastapi import HTTPException
from typing import override
from collections.abc import Sequence
from shared.base_controller import BaseRepository
from .models import (
    User,
    UserRole,
    UserIdentity,
    UserRoleUserLink,
)

from .schemes import UserCreate, UserUpdate, UserUpdateDict


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    @override
    def get_all(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        statement = (
            select(User).where(User.roles.any(name="Admin")).offset(offset).limit(limit)
        )
        users = db.exec(statement).all()
        return users

    @override
    def create(self, db: Session, obj_in: UserCreate) -> User:
        # Crear una instancia de User
        user: User = User(
            **obj_in.model_dump(exclude={"role_ids", "username", "password"})
        )
        # Crear la identidad asociada
        identity: UserIdentity = UserIdentity(
            username=obj_in.username,
            password=obj_in.password,
            user_id=user.id,
        )
        user.identity = identity

        if obj_in.role_ids:
            roles = db.exec(
                select(UserRole).where(UserRole.id.in_(obj_in.role_ids))
            ).all()
            user.roles = roles

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @override
    def update(self, db: Session, id: str, obj_in: UserUpdate) -> User:
        user: User | None = db.get(self.model, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Obtener los datos de actualización excluyendo los no establecidos
        obj_data: dict[str, object] = obj_in.model_dump(exclude_unset=True)

        user.sqlmodel_update(obj_data)

        if "username" in obj_data or "password" in obj_data:
            if user.identity:
                if "username" in obj_data:
                    user.identity.username = obj_data["username"]
                if "password" in obj_data:
                    user.identity.password = obj_data["password"]
            else:
                if "username" in obj_data and "password" in obj_data:
                    identity = UserIdentity(
                        username=obj_data["username"],
                        password=obj_data["password"],
                        user_id=user.id,
                    )
                    user.identity = identity

        if "role_ids" in obj_data:
            roles = db.exec(
                select(UserRole).where(UserRole.id.in_(obj_data["role_ids"]))
            ).all()
            user.roles = roles

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @override
    def delete(self, db: Session, id: str) -> User:
        user: User | None = db.get(self.model, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Eliminar las relaciones en la tabla de enlace UserRoleUserLink
        links = db.exec(
            select(UserRoleUserLink).where(UserRoleUserLink.user_id == id)
        ).all()
        for link in links:
            db.delete(link)

        # Eliminar la identidad asociada
        if user.identity:
            db.delete(user.identity)

        # Eliminar el usuario
        db.delete(user)
        db.commit()
        return user
