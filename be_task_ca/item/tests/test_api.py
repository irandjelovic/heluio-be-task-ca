from unittest.mock import Mock, patch
from uuid import UUID

from starlette.testclient import TestClient

from be_task_ca.app import app
from be_task_ca.item.entities import Item
from be_task_ca.item.exceptions import ItemDuplicateError
from be_task_ca.item.schema import CreateItemRequest


@patch("be_task_ca.item.api.create_item")
def test_post_item_success(mock_post_item: Mock):
    new_item = Item(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        name="New Item",
        description="Description",
        price=10.99,
        quantity=100,
    )
    mock_post_item.return_value = new_item

    client = TestClient(app)
    item_data = CreateItemRequest(
        name="New Item", description="Description", price=10.99, quantity=100
    )
    response = client.post("/items/", json=item_data.dict())

    assert response.status_code == 200
    assert response.json() == {
        "id": str(new_item.id),
        "name": new_item.name,
        "description": new_item.description,
        "price": new_item.price,
        "quantity": new_item.quantity,
    }


@patch(
    "be_task_ca.item.api.create_item", side_effect=ItemDuplicateError("Error duplicate")
)
def test_post_item_duplicate(mock_post_item: Mock):
    item_data = CreateItemRequest(
        name="Duplicate Item", description="Description", price=10.99, quantity=100
    )

    client = TestClient(app)
    response = client.post("/items/", json=item_data.dict())

    assert response.status_code == 409
    assert response.json() == {"detail": "Error duplicate"}
