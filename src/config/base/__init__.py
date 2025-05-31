from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from src.entities.user.models import UserRole
from src.entities.state.models import State

# Configuración de la base de datos
SQLITE_FILE_NAME = "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"
CONNECT_ARGS = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, connect_args=CONNECT_ARGS)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    create_default_users()
    create_default_states()


def create_default_users():
    with Session(engine) as session:
        if session.query(UserRole).count() == 0:
            users = [
                UserRole(name="Admin"),
                UserRole(name="User"),
                UserRole(name="Master"),
            ]
            session.add_all(users)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


def create_default_states():
    with Session(engine) as session:
        if session.query(State).count() == 0:
            states = [
                State(nombre="Activo", descripcion="Usuario activo"),
                State(nombre="Inactivo", descripcion="Usuario inactivo"),
                State(nombre="Suspendido", descripcion="Usuario suspendido"),
            ]
            session.add_all(states)
            session.commit()


SessionDep = Annotated[Session, Depends(get_session)]
