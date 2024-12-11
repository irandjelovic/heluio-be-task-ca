from typing import Type
from unittest.mock import Mock
from uuid import UUID

import pytest

from be_task_ca.item.entities import Item
from be_task_ca.item.exceptions import ItemDuplicateError
from be_task_ca.item.usecases import create_item


@pytest.mark.parametrize(
    "name_exists, expected_exception, saved_item",
    [
        (
            False,
            None,
            Item(name="Test Item", id=UUID("123e4567-e89b-12d3-a456-426614174000")),
        ),
        (True, ItemDuplicateError, None),
    ],
)
def test_create_item(
    name_exists: bool,
    expected_exception: Type[Exception],
    saved_item: Item,
    mock_repo: Mock,
):
    item: Item = Item(id=UUID("123e4567-e89b-12d3-a456-426614174000"), name="Test Item")

    mock_repo.find_item_by_name.return_value = (
        None if not name_exists else Item(name=item.name)
    )
    mock_repo.save_item.return_value = saved_item

    if expected_exception:
        with pytest.raises(expected_exception):
            create_item(item, mock_repo)
    else:
        created_item: Item = create_item(item, mock_repo)

        assert created_item.name == item.name
        assert created_item.id == item.id
        mock_repo.save_item.assert_called_once_with(item)
