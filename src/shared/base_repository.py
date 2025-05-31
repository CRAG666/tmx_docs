from typing import Generic
from collections.abc import Sequence
from sqlmodel import select, Session
from fastapi import HTTPException
from .base_types import (
    ModelType,
    CreateSchemaType,
    UpdateSchemaType,
)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository class for handling common database operations."""

    def __init__(self, model: type[ModelType]):
        """Initializes the repository with a specific SQLModel class.

        Args:
            model: The SQLModel class for the entity.
        """
        self.model: type[ModelType] = model

    def get_by_id(self, db: Session, id: str) -> ModelType | None:
        """Fetches a record by its ID.

        Args:
            db: Database session.
            id: The ID of the record.

        Returns:
            The model instance if found, else None.
        """
        try:
            return db.get(self.model, id)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching record: {str(e)}"
            )

    def get_all(
        self,
        db: Session,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """Retrieves a list of records with pagination.

        Args:
            db: Database session.
            offset: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A sequence of model instances.
        """
        try:
            return (
                db.exec(select(self.model).offset(offset).limit(limit)).unique().all()
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching records: {str(e)}"
            )

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Creates a new record in the database.

        Args:
            db: Database session.
            obj_in: The data for the new record.

        Returns:
            The newly created model instance.
        """
        try:
            db_obj = self.model.model_validate(obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error creating record: {str(e)}"
            )

    def update(
        self,
        db: Session,
        id: str,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        """Updates an existing record.

        Args:
            db: Database session.
            id: The ID of the record to update.
            obj_in: The updated data.

        Returns:
            The updated model instance.

        Raises:
            HTTPException: If the record is not found.
        """
        try:
            obj_db = db.get(self.model, id)
            if not obj_db:
                raise HTTPException(status_code=404, detail="Record not found")

            obj_data = obj_in.model_dump(exclude_unset=True)
            obj_db.sqlmodel_update(obj_data)
            db.add(obj_db)
            db.commit()
            db.refresh(obj_db)
            return obj_db
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error updating record: {str(e)}"
            )

    def delete(self, db: Session, id: str) -> ModelType:
        """Deletes a record by its ID.

        Args:
            db: Database session.
            id: The ID of the record to delete.

        Returns:
            The deleted model instance.

        Raises:
            HTTPException: If the record is not found.
        """
        try:
            obj_db = db.get(self.model, id)
            if not obj_db:
                raise HTTPException(status_code=404, detail="Record not found")

            db.delete(obj_db)
            db.commit()
            return obj_db
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error deleting record: {str(e)}"
            )
