import pytest
from helpers import (
    register_new_courier_and_return_login_password,
    login_courier_and_return_id,
    delete_courier,
    create_order_and_return_track,
    cancel_order
)


@pytest.fixture
def courier_data():
    """Фикстура создаёт курьера и удаляет после теста."""
    data = register_new_courier_and_return_login_password()
    yield data
    if data:
        courier_id = login_courier_and_return_id(data[0], data[1])
        if courier_id:
            delete_courier(courier_id)


@pytest.fixture
def order_track():
    """Фикстура создаёт заказ и отменяет после теста."""
    track = create_order_and_return_track()
    yield track
    if track:
        cancel_order(track)