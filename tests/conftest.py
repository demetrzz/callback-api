import asyncio
from datetime import UTC, datetime
from httpx import ASGITransport, AsyncClient
import pytest
from app.db import SessionLocal, engine
from app.models import Base, Product, Reservation
from app.schemas import ReservationStatusEnum
from app.main import app as fastapi_app


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        product = Product(id=1, quantity=100)
        reservation1 = Reservation(
            id=1,
            quantity=10,
            status=ReservationStatusEnum.created,
            product_id=product.id,
            timestamp=datetime.now(UTC),
        )
        reservation2 = Reservation(
            id=2,
            quantity=10,
            status=ReservationStatusEnum.cancelled,
            product_id=product.id,
            timestamp=datetime.now(UTC),
        )
        reservation3 = Reservation(
            id=3,
            quantity=10,
            status=ReservationStatusEnum.success,
            product_id=product.id,
            timestamp=datetime.now(UTC),
        )
        session.add_all([product, reservation1, reservation2, reservation3])
        await session.commit()


@pytest.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(fastapi_app),
        base_url="http://localhost:8000",
    ) as async_client:
        yield async_client
