from sqlmodel import SQLModel

from typing import TypeVar

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=SQLModel)
