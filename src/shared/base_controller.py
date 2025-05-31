from typing import Final, Annotated
from fastapi import HTTPException, FastAPI, status, Query
from .base_types import (
    ModelType,
    CreateSchemaType,
    UpdateSchemaType,
)
from sqlmodel import SQLModel
from src.config.base import SessionDep
from .base_repository import BaseRepository


class ControllerBuilder:
    """Dynamic REST controller builder for SQLModel-based models.

    This class allows registering CRUD routes on a FastAPI app using a generic repository
    and schema definitions. It provides a flexible way to enable only the desired endpoints.
    """

    def __init__(
        self,
        repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType],
        path_name: str,
        response_schema: type[SQLModel],
    ):
        """Initializes the controller with base components.

        Args:
            repository: The repository instance with CRUD operations.
            path_name: The base path for routes (e.g., "users").
            response_schema: The output schema used in route responses.
        """
        self.repository: Final = repository
        self.path_name: Final = path_name
        self.response_schema: type[SQLModel] = response_schema
        self.create_schema: type[SQLModel] | None = None
        self.update_schema: type[SQLModel] | None = None
        self.methods: set[str] = set()

    def enable_get(self):
        """Enables the GET /{path}/ endpoint to fetch all items."""
        if "GET" in self.methods:
            raise ValueError("GET endpoint is already enabled.")
        self.methods.add("GET")
        return self

    def enable_get_by_id(self):
        """Enables the GET /{path}/{id} endpoint to fetch an item by ID."""
        if "GETID" in self.methods:
            raise ValueError("GET by ID endpoint is already enabled.")
        self.methods.add("GETID")
        return self

    def enable_create(self, schema: type[SQLModel]):
        """Enables the POST /{path}/ endpoint to create a new item."""
        if "POST" in self.methods:
            raise ValueError("POST endpoint is already enabled.")
        self.create_schema = schema
        self.methods.add("POST")
        return self

    def enable_update(self, schema: type[SQLModel]):
        """Enables the PATCH /{path}/{id} endpoint to partially update an item."""
        if "PATCH" in self.methods:
            raise ValueError("PATCH endpoint is already enabled.")
        self.update_schema = schema
        self.methods.add("PATCH")
        return self

    def enable_put(self, schema: type[SQLModel]):
        """Enables the PUT /{path}/{id} endpoint to fully replace an item."""
        if "PUT" in self.methods:
            raise ValueError("PUT endpoint is already enabled.")
        self.update_schema = schema
        self.methods.add("PUT")
        return self

    def enable_delete(self):
        """Enables the DELETE /{path}/{id} endpoint to delete an item."""
        if "DELETE" in self.methods:
            raise ValueError("DELETE endpoint is already enabled.")
        self.methods.add("DELETE")
        return self

    def enable_read_only(self):
        """Enables only read operations: GET and GET by ID."""
        return self.enable_get().enable_get_by_id()

    def enable_full_crud(
        self,
        create_schema: type[SQLModel],
        update_schema: type[SQLModel],
    ):
        """Enables all CRUD operations: GET, POST, PATCH, DELETE.

        Args:
            create_schema: Schema for creating items (used in POST).
            update_schema: Schema for updating items (used in PATCH and PUT).
        """
        return (
            self.enable_get()
            .enable_get_by_id()
            .enable_create(create_schema)
            .enable_update(update_schema)
            .enable_delete()
        )

    def enable_write_only(
        self,
        create_schema: type[SQLModel],
        update_schema: type[SQLModel],
    ):
        """Enables only write operations: POST, PATCH, DELETE.

        Args:
            create_schema: Schema for creating items (used in POST).
            update_schema: Schema for updating items (used in PATCH and PUT).
        """
        return (
            self.enable_create(create_schema)
            .enable_update(update_schema)
            .enable_delete()
        )

    def register_routes(self, app: FastAPI):
        """Registers the enabled routes in the given FastAPI app.

        Args:
            app: The FastAPI app where routes will be registered.

        Raises:
            ValueError: If `response_schema` is not set or required schemas are missing
                based on the enabled endpoints.
        """
        if not self.response_schema:
            raise ValueError("response_schema is required")

        self._validate_schema_dependencies()

        method_to_register = {
            "GET": self.__register_get_all,
            "GETID": self.__register_get_by_id,
            "POST": self.__register_create,
            "PATCH": self.__register_update,
            "PUT": self.__register_put,
            "DELETE": self.__register_delete,
        }

        for method in self.methods:
            if method in method_to_register:
                method_to_register[method](app)

    def _validate_schema_dependencies(self):
        """Validates that required schemas are defined for enabled endpoints.

        Raises:
            ValueError: If POST is enabled without a `create_schema`, or
                if PATCH or PUT is enabled without an `update_schema`.
        """
        if "POST" in self.methods and not self.create_schema:
            raise ValueError("POST endpoint requires create_schema")

        if (
            "PATCH" in self.methods or "PUT" in self.methods
        ) and not self.update_schema:
            raise ValueError("PATCH/PUT endpoint requires update_schema")

    # ——— Private methods for route registration ———

    def __register_get_all(self, app: FastAPI):
        """Registers the GET /{path}/ endpoint."""

        @app.get(f"/{self.path_name}/", response_model=list[self.response_schema])
        def _(
            session: SessionDep,
            offset: int = 0,
            limit: Annotated[int, Query(le=100)] = 100,
        ):
            return self.repository.get_all(session, offset, limit)

    def __register_get_by_id(self, app: FastAPI):
        """Registers the GET /{path}/{id} endpoint."""

        @app.get(f"/{self.path_name}/{{id}}", response_model=self.response_schema)
        def _(id: str, session: SessionDep):
            item = self.repository.get_by_id(session, id)
            if item is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.path_name} with ID {id} not found",
                )
            return item

    def __register_create(self, app: FastAPI):
        """Registers the POST /{path}/ endpoint."""

        @app.post(
            f"/{self.path_name}/",
            response_model=self.response_schema,
            status_code=status.HTTP_201_CREATED,
        )
        def _(item_in: self.create_schema, session: SessionDep):
            return self.repository.create(session, item_in)

    def __register_update(self, app: FastAPI):
        """Registers the PATCH /{path}/{id} endpoint."""

        @app.patch(f"/{self.path_name}/{{id}}", response_model=self.response_schema)
        def _(id: str, obj: self.update_schema, session: SessionDep):
            return self.repository.update(session, id, obj)

    def __register_put(self, app: FastAPI):
        """Registers the PUT /{path}/{id} endpoint."""

        @app.put(f"/{self.path_name}/{{id}}", response_model=self.response_schema)
        def _(id: str, obj: self.update_schema, session: SessionDep):
            return self.repository.update(session, id, obj)

    def __register_delete(self, app: FastAPI):
        """Registers the DELETE /{path}/{id} endpoint."""

        @app.delete(
            f"/{self.path_name}/{{id}}",
            response_model=self.response_schema,
            status_code=status.HTTP_200_OK,
        )
        def _(id: str, session: SessionDep):
            return self.repository.delete(session, id)
