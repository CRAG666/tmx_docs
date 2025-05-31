from src.shared.base_controller import ControllerBuilder
from src.shared.base_repository import BaseRepository
from src.entities.device.repository import DeviceRelationRepository, DeviceRepository
from src.entities.device.models import Device, DeviceRelation
from src.entities.device.schemes import (
    DeviceCreate,
    DeviceUpdate,
    DevicePublic,
    DeviceRelationCreate,
    DeviceRelationPublic,
    DeviceRelationUpdate,
)


# Inicializar el repositorio
device_relation_repository = DeviceRelationRepository(model=DeviceRelation)

device_relation_controller = ControllerBuilder(
    repository=device_relation_repository,
    response_schema=DeviceRelationPublic,
    path_name="device_relation",
).enable_full_crud(
    update_schema=DeviceRelationUpdate, create_schema=DeviceRelationCreate
)

device_repository = DeviceRepository(model=Device)


device_controller = ControllerBuilder(
    repository=device_repository,
    response_schema=DevicePublic,
    path_name="device",
).enable_full_crud(update_schema=DeviceUpdate, create_schema=DeviceCreate)
