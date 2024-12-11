from typing import Type
from unittest.mock import patch, Mock
from uuid import UUID

import pytest

from be_task_ca.user.entities import User, CartItem
from be_task_ca.item.service import Item
from be_task_ca.user.exceptions import (
    UserNotExistsError,
    ItemsNotEnoughError,
    ItemAlreadyAdded,
    ItemNotExistsError,
    UserEmailDuplicateError,
)
from be_task_ca.user.usecases import add_item_to_cart, create_user


@pytest.mark.parametrize(
    "email_exists, expected_exception, saved_user",
    [
        (
            False,
            None,
            User(
                email="test@example.com",
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            ),
        ),
        (True, UserEmailDuplicateError, None),
    ],
)
def test_create_user(
    email_exists: bool,
    expected_exception: Type[Exception],
    saved_user: User,
    mock_repo: Mock,
):
    user = User(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"), email="test@example.com"
    )

    mock_repo.find_user_by_email.return_value = (
        None if not email_exists else User(email=user.email)
    )
    mock_repo.save_user.return_value = saved_user

    if expected_exception:
        with pytest.raises(expected_exception):
            create_user(user, mock_repo)
    else:
        created_user: User = create_user(user, mock_repo)

        assert created_user.email == user.email
        assert created_user.id == user.id
        mock_repo.save_user.assert_called_once_with(user)


@pytest.mark.parametrize(
    "user_exists, item_exists, item_quantity, cart_item_quantity, expected_exception, new_cart_item",
    [
        (
            True,
            True,
            10,
            5,
            None,
            CartItem(item_id=UUID("987e4567-e89b-12d3-a456-426614174112"), quantity=5),
        ),
        (False, True, 10, 5, UserNotExistsError, None),
        (True, False, 10, 5, ItemNotExistsError, None),
        (True, True, 10, 15, ItemsNotEnoughError, None),
        (
            True,
            True,
            10,
            5,
            ItemAlreadyAdded,
            CartItem(item_id=UUID("987e4567-e89b-12d3-a456-426614174111")),
        ),
    ],
)
def test_add_item_to_cart(
    user_exists: bool,
    item_exists: bool,
    item_quantity: int,
    cart_item_quantity: int,
    new_cart_item: CartItem,
    mock_repo: Mock,
    expected_exception: Type[Exception],
):
    user: User = User(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"), cart_items=[new_cart_item]
    )
    item: Item = Item(
        id=UUID("987e4567-e89b-12d3-a456-426614174111"), quantity=item_quantity
    )
    cart_item: CartItem = CartItem(
        item_id=UUID("987e4567-e89b-12d3-a456-426614174111"),
        quantity=cart_item_quantity,
    )

    with patch.object(
        mock_repo, "find_user_by_id", return_value=user if user_exists else None
    ), patch(
        "be_task_ca.user.usecases.find_item_by_id",
        return_value=item if item_exists else None,
    ), patch.object(
        mock_repo, "save_user", return_value=None
    ):
        if expected_exception:
            with pytest.raises(expected_exception):
                add_item_to_cart(user.id, cart_item, mock_repo)
        else:
            added_cart_item: CartItem = add_item_to_cart(user.id, cart_item, mock_repo)

            assert added_cart_item.item_id == cart_item.item_id
            assert added_cart_item.quantity == cart_item.quantity
            mock_repo.save_user.assert_called_once_with(user)
