from sqlmodel import Session, select
from fastapi import HTTPException
from typing import override
from collections.abc import Sequence
from src.shared.base_repository import BaseRepository

from .models import DeviceRelation
from .schemes import DeviceRelationCreate, DeviceRelationUpdate

from .models import Device
from .schemes import DeviceCreate, DeviceUpdate

from src.entities.state.models import State


class DeviceRelationRepository(
    BaseRepository[DeviceRelation, DeviceRelationCreate, DeviceRelationUpdate]
):
    @override
    def create(self, db: Session, obj_in: DeviceRelationCreate) -> DeviceRelation:
        # Verificar existencia de la instancia
        id1 = self.get_by_id(db, obj_in.device_id1)
        id2 = self.get_by_id(db, obj_in.device_id2)
        # Crear una instancia de DeviceRelation
        if id1 and id2:
            return super().create(db, obj_in)
        raise HTTPException(status_code=404, detail="IDs no validos")

    @override
    def update(
        self, db: Session, id: str, obj_in: DeviceRelationUpdate
    ) -> DeviceRelation:
        if obj_in.device_id1:
            id1 = self.get_by_id(db, obj_in.device_id1)
            if not id1:
                raise HTTPException(status_code=404, detail="ID1 no valido")
        if obj_in.device_id2:
            id2 = self.get_by_id(db, obj_in.device_id2)
            if not id2:
                raise HTTPException(status_code=404, detail="ID2 no valido")
        return super().update(db, id, obj_in)


class DeviceRepository(BaseRepository[Device, DeviceCreate, DeviceUpdate]):
    @override
    def create(self, db: Session, obj_in: DeviceCreate) -> Device:
        # Verificar existencia de la instancia
        estado = db.get(State, obj_in.state_id)
        # Crear una instancia de DeviceRelation
        if estado:
            return super().create(db, obj_in)
        raise HTTPException(status_code=404, detail="Datos no validos")

    @override
    def update(self, db: Session, id: str, obj_in: DeviceUpdate) -> Device:
        if obj_in.state_id:
            estado = db.get(State, obj_in.state_id)
            if not estado:
                raise HTTPException(status_code=404, detail="Estado no valido")
        return super().update(db, id, obj_in)
