from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ReservationStatusEnum(str, Enum):
    created = "created"
    success = "success"
    error = "error"
    cancelled = "cancelled"


class CreateReservation(BaseModel):
    reservation_id: int
    product_id: int
    quantity: int = Field(ge=1)
    timestamp: datetime


class CreateReservationResponse(BaseModel):
    status: ReservationStatusEnum
    message: str | None
    reservation_id: str


class ReservationStatusResponse(BaseModel):
    reservation_id: str
    status: ReservationStatusEnum
