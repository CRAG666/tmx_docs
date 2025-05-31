from sqlmodel import SQLModel
from typing import TypedDict
from datetime import datetime


class DeviceCreate(SQLModel):
    state_id: str
    nombre: str
    serial_number: str
    password_hash: str


class DeviceUpdate(SQLModel):
    state_id: str | None
    nombre: str | None
    serial_number: str | None
    password_hash: str | None


class DevicePublic(SQLModel):
    id: str
    state_id: str
    nombre: str
    created_at: datetime

    # Relaciones
    current_state: str


class DeviceRelationCreate(SQLModel):
    device_id1: str
    device_id2: str
    relation_type: str


class DeviceRelationUpdate(SQLModel):
    device_id1: str | None
    device_id2: str | None
    relation_type: str | None


class DeviceRelationPublic(SQLModel):
    id: str
    device_id1: str
    device_id2: str
    relation_type: str
    created_at: datetime


# ================================================
# Relación Dispositivo-Service
# ================================================
# class DeviceService(SQLModel):
#    device_id: str
#    service_id: str
#    start_date: datetime | None
#    end_date: datetime | None


# class DeviceServicePublic(SQLModel):
#    id: str
#    device_id: str
#    service_id: str
#    start_date: datetime | None
#    end_date: datetime | None
#   created_at: datetime

# Relaciones
# device: Device
