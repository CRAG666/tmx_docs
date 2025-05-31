from sqlmodel import SQLModel, Field, Relationship
from src.config.base.utils import get_uuid
from datetime import datetime
from src.entities.state.models import State


# ================================================
# Dispositivos
# ================================================
class Device(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    state_id: str = Field(foreign_key="state.id")
    nombre: str = Field(max_length=100, index=True)
    serial_number: str = Field(max_length=50, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    state: State = Relationship(back_populates="devices")
    device_relations_1: list["DeviceRelation"] = Relationship(
        back_populates="device1",
        sa_relationship_kwargs={"foreign_keys": "[DeviceRelation.device_id1]"},
    )
    device_relations_2: list["DeviceRelation"] = Relationship(
        back_populates="device2",
        sa_relationship_kwargs={"foreign_keys": "[DeviceRelation.device_id2]"},
    )
    # device_services: list["DeviceService"] = Relationship(
    #    back_populates="device")

    @property
    def current_state(self):
        if self.state:
            return self.state.nombre
        return ""


class DeviceRelation(SQLModel, table=True):
    id: str = Field(default_factory=get_uuid, primary_key=True)
    device_id1: str = Field(foreign_key="device.id")
    device_id2: str = Field(foreign_key="device.id")
    relation_type: str = Field(max_length=50)  # Ej: "parent", "sibling"
    created_at: datetime = Field(default_factory=datetime.now)

    # Relaciones
    device1: Device = Relationship(
        back_populates="device_relations_1",
        sa_relationship_kwargs={"foreign_keys": "[DeviceRelation.device_id1]"},
    )
    device2: Device = Relationship(
        back_populates="device_relations_2",
        sa_relationship_kwargs={"foreign_keys": "[DeviceRelation.device_id2]"},
    )


# ================================================
# Relación Dispositivo-Service
# ================================================
# class DeviceService(SQLModel, table=True):
#    id: str = Field(default_factory=get_uuid, primary_key=True)
#    device_id: str = Field(foreign_key="device.id")
# service_id: str = Field(foreign_key="organizationservice.id")
#    start_date: datetime | None = None
#    end_date: datetime | None = None
#    created_at: datetime = Field(default_factory=datetime.now)

# Relaciones
#    device: Device = Relationship(back_populates="device_services")
# service: OrganizationService = Relationship(
# back_populates="device_services")
# role_permissions: list["RoleDevicePermission"] = Relationship(
#    back_populates="device_service"
# )
