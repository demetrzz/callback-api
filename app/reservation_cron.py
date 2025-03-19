import asyncio
from datetime import UTC, datetime, timedelta
from sqlalchemy import select
from app.db import SessionLocal
from app.schemas import ReservationStatusEnum
from app.models import Product, Reservation


async def process_expired_reservations():
    print("running reservations check")
    async with SessionLocal() as session:
        cutoff = datetime.now(UTC) - timedelta(minutes=5)
        result = await session.execute(
            select(Reservation)
            .where(
                Reservation.status == ReservationStatusEnum.created,
                Reservation.timestamp < cutoff,
            )
            .with_for_update()
        )
        reservations = result.scalars().all()
        for reservation in reservations:
            print(f"Cancelling reservation {reservation.id}")
            reservation.status = ReservationStatusEnum.cancelled
            product = await session.get(
                Product, reservation.product_id, with_for_update=True
            )
            if product:
                product.quantity += reservation.quantity
        await session.commit()


async def main():
    while True:
        try:
            await process_expired_reservations()
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
