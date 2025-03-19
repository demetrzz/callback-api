from datetime import UTC, datetime
from httpx import AsyncClient
import pytest

from app.schemas import ReservationStatusEnum


@pytest.mark.parametrize(
    ("data", "status_response", "status_code"),
    [
        (
            {
                "reservation_id": "123",
                "product_id": "123",
                "quantity": 10,
                "timestamp": str(datetime.now(UTC)),
            },
            ReservationStatusEnum.error,
            404,
        ),
        (
            {
                "reservation_id": "123",
                "product_id": "1",
                "quantity": 1000,
                "timestamp": str(datetime.now(UTC)),
            },
            ReservationStatusEnum.error,
            409,
        ),
        (
            {
                "reservation_id": "1",
                "product_id": "1",
                "quantity": 10,
                "timestamp": str(datetime.now(UTC)),
            },
            ReservationStatusEnum.error,
            429,
        ),
        (
            {
                "reservation_id": "123",
                "product_id": "1",
                "quantity": 10,
                "timestamp": str(datetime.now(UTC)),
            },
            ReservationStatusEnum.created,
            201,
        ),
    ],
)
async def test_create_reservation(
    data, status_response, status_code, prepare_db, async_client: AsyncClient
):
    response = await async_client.post("/api/v1/reserve", json=data)
    assert response.status_code == status_code
    assert response.json()["status"] == status_response


@pytest.mark.parametrize(
    ("reservation_id", "status_response", "status_code"),
    [
        (
            "123",
            ReservationStatusEnum.error,
            404,
        ),
        (
            "1",
            ReservationStatusEnum.created,
            200,
        ),
    ],
)
async def test_get_reservation(
    reservation_id, status_response, status_code, prepare_db, async_client: AsyncClient
):
    response = await async_client.get(
        "/api/v1/reservation", params={"reservation_id": reservation_id}
    )
    assert response.status_code == status_code
    assert response.json()["status"] == status_response


@pytest.mark.parametrize(
    ("reservation_id", "status_response", "status_code"),
    [
        (
            "123",
            ReservationStatusEnum.error,
            404,
        ),
        (
            "1",
            ReservationStatusEnum.cancelled,
            200,
        ),
        (
            "2",
            ReservationStatusEnum.cancelled,
            409,
        ),
    ],
)
async def test_cancel_reservation(
    reservation_id, status_response, status_code, prepare_db, async_client: AsyncClient
):
    response = await async_client.patch(
        "/api/v1/cancel_reservation", params={"reservation_id": reservation_id}
    )
    assert response.status_code == status_code
    assert response.json()["status"] == status_response


@pytest.mark.parametrize(
    ("reservation_id", "status_response", "status_code"),
    [
        (
            "123",
            ReservationStatusEnum.error,
            404,
        ),
        (
            "1",
            ReservationStatusEnum.success,
            200,
        ),
        (
            "2",
            ReservationStatusEnum.cancelled,
            409,
        ),
    ],
)
async def test_approve_reservation(
    reservation_id, status_response, status_code, prepare_db, async_client: AsyncClient
):
    response = await async_client.patch(
        "/api/v1/approve_reservation", params={"reservation_id": reservation_id}
    )
    assert response.status_code == status_code
    assert response.json()["status"] == status_response
