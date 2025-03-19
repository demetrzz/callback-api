from datetime import UTC, datetime, timedelta

from app.db import SessionLocal
from app.models import Product, Reservation
from app.reservation_cron import process_expired_reservations
from app.schemas import ReservationStatusEnum


async def test_expired_reservation_cancelled(prepare_db):
    async with SessionLocal() as session:
        product = await session.get(Product, 1)
        old_quant = product.quantity
        old_time = datetime.now(UTC) - timedelta(minutes=10)
        reservation = await session.get(Reservation, 1)
        reservation.timestamp = old_time
        await session.commit()
        reservation_id = reservation.id

    await process_expired_reservations()

    async with SessionLocal() as session:
        reservation = await session.get(Reservation, reservation_id)
        assert reservation.status == ReservationStatusEnum.cancelled

        product = await session.get(Product, 1)
        assert product.quantity == old_quant + reservation.quantity
