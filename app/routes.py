from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Product, Reservation
from app.schemas import (
    CreateReservation,
    CreateReservationResponse,
    ReservationStatusEnum,
)


api_router = APIRouter(prefix="/api/v1")


@api_router.post("/reserve", response_model=CreateReservationResponse)
async def create_reservation(
    reservation_data: CreateReservation, session: AsyncSession = Depends(get_db)
):
    product = await session.get(
        Product, reservation_data.product_id, with_for_update=True
    )
    if not product:
        return JSONResponse(
            status_code=404,
            content={
                "status": ReservationStatusEnum.error,
                "message": "Product doesnt exist",
                "reservation_id": str(reservation_data.reservation_id),
            },
        )
    if product.quantity < reservation_data.quantity:
        return JSONResponse(
            status_code=409,
            content={
                "status": ReservationStatusEnum.error,
                "message": "Not enough stock available",
                "reservation_id": str(reservation_data.reservation_id),
            },
        )
    product.quantity -= reservation_data.quantity
    reservation = Reservation(
        id=reservation_data.reservation_id,
        quantity=reservation_data.quantity,
        status=ReservationStatusEnum.created,
        product_id=reservation_data.product_id,
        timestamp=reservation_data.timestamp,
    )
    session.add(reservation)
    try:
        await session.commit()
    except Exception as err:
        message = "Error saving data"
        print(message, err)
        return JSONResponse(
            status_code=429,
            content={
                "status": ReservationStatusEnum.error,
                "message": message,
                "reservation_id": str(reservation_data.reservation_id),
            },
        )
    return JSONResponse(
        status_code=201,
        content={
            "status": ReservationStatusEnum.created,
            "message": "Reservation created successfully",
            "reservation_id": str(reservation_data.reservation_id),
        },
    )


@api_router.get("/reservation", response_model=CreateReservationResponse)
async def get_reservation(reservation_id: int, session: AsyncSession = Depends(get_db)):
    reservation = await session.get(Reservation, reservation_id)
    if not reservation:
        return JSONResponse(
            status_code=404,
            content={
                "status": ReservationStatusEnum.error,
                "message": "Reservation doesnt exist",
                "reservation_id": str(reservation_id),
            },
        )
    return JSONResponse(
        status_code=200,
        content={
            "status": reservation.status,
            "reservation_id": str(reservation_id),
        },
    )


@api_router.patch("/cancel_reservation", response_model=CreateReservationResponse)
async def cancel_reservation(
    reservation_id: int, session: AsyncSession = Depends(get_db)
):
    reservation = await session.get(Reservation, reservation_id, with_for_update=True)
    if not reservation:
        return JSONResponse(
            status_code=404,
            content={
                "status": ReservationStatusEnum.error,
                "message": "Reservation doesnt exist",
                "reservation_id": str(reservation_id),
            },
        )
    if reservation.status != ReservationStatusEnum.created:
        return JSONResponse(
            status_code=409,
            content={
                "status": reservation.status,
                "message": "Reservation is already in final status",
                "reservation_id": str(reservation_id),
            },
        )
    product = await session.get(Product, reservation.product_id, with_for_update=True)
    product.quantity += reservation.quantity
    reservation.status = ReservationStatusEnum.cancelled
    await session.commit()
    return JSONResponse(
        status_code=200,
        content={
            "status": ReservationStatusEnum.cancelled,
            "message": "Reservation cancelled successfully",
            "reservation_id": str(reservation_id),
        },
    )


@api_router.patch("/approve_reservation", response_model=CreateReservationResponse)
async def approve_reservation(
    reservation_id: int, session: AsyncSession = Depends(get_db)
):
    reservation = await session.get(Reservation, reservation_id, with_for_update=True)
    if not reservation:
        return JSONResponse(
            status_code=404,
            content={
                "status": ReservationStatusEnum.error,
                "message": "Reservation doesnt exist",
                "reservation_id": str(reservation_id),
            },
        )
    if reservation.status != ReservationStatusEnum.created:
        return JSONResponse(
            status_code=409,
            content={
                "status": reservation.status,
                "message": "Reservation is already in final status",
                "reservation_id": str(reservation_id),
            },
        )
    reservation.status = ReservationStatusEnum.success
    await session.commit()
    return JSONResponse(
        status_code=200,
        content={
            "status": ReservationStatusEnum.success,
            "message": "Reservation approved successfully",
            "reservation_id": str(reservation_id),
        },
    )
