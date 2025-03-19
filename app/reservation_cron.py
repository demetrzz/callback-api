import asyncio
from datetime import UTC, datetime, timedelta
from sqlalchemy import select, update
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
        print(
            f"Cancelling reservations {[reservation.id for reservation in reservations]}"
        )
        product_updates = {}
        for reservation in reservations:
            product_updates[reservation.product_id] = (
                product_updates.get(reservation.product_id, 0) + reservation.quantity
            )
            reservation.status = ReservationStatusEnum.cancelled
        for product_id, quantity in product_updates.items():
            await session.execute(
                update(Product)
                .where(Product.id == product_id)
                .values(quantity=Product.quantity + quantity)
            )
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
