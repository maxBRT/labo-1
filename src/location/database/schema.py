from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from decimal import Decimal


# Pydantic models for linking the database with the ui
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ClientBase(BaseSchema):
    name: str
    email: str
    phone: str


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int


class EquipmentBase(BaseSchema):
    name: str
    cost_per_day: Decimal
    is_available: bool


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: int


class LocationBase(BaseSchema):
    start_date: datetime
    end_date: datetime
    is_returned: bool


class LocationCreate(LocationBase):
    id_client: int
    id_equipment: int


class LocationRead(LocationBase):
    id: int
    client: ClientRead
    equipment: EquipmentRead
