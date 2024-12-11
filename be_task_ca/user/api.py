import hashlib
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from .entities import User, CartItem
from .exceptions import (
    UserEmailDuplicateError,
    UserNotExistsError,
    ItemNotExistsError,
    ItemsNotEnoughError,
    ItemAlreadyAdded,
)
from .repository.repository import Repository
from .repository.repository_db import RepositoryDb
from .repository.repository_im import RepositoryIM
from .schema import (
    AddToCartRequest,
    CreateUserRequest,
    CreateUserResponse,
    AddToCartResponse,
)
from .usecases import add_item_to_cart, create_user, list_items_in_cart
from ..settings import settings

user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


def get_repo() -> Repository:
    db: str = settings.tool.project_config.db
    if db == "memory":
        return RepositoryIM()
    return RepositoryDb(db_url=db)


@user_router.post("/")
async def post_customer(
    user: CreateUserRequest, repo: Repository = Depends(get_repo)
) -> CreateUserResponse:
    user_payload: User = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashlib.sha512(user.password.encode("UTF-8")).hexdigest(),
        shipping_address=user.shipping_address,
    )

    try:
        created_user: User = create_user(user_payload, repo)
    except UserEmailDuplicateError as ex:
        raise HTTPException(status_code=409, detail=str(ex))

    return CreateUserResponse(
        id=created_user.id,
        first_name=created_user.first_name,
        last_name=created_user.last_name,
        email=created_user.email,
        shipping_address=created_user.shipping_address,
    )


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID, cart_item: AddToCartRequest, repo: Repository = Depends(get_repo)
) -> AddToCartResponse:
    cart_item_payload: CartItem = CartItem(
        user_id=user_id, item_id=cart_item.item_id, quantity=cart_item.quantity
    )

    try:
        new_cart_item: CartItem = add_item_to_cart(user_id, cart_item_payload, repo)
    except (UserNotExistsError, ItemNotExistsError) as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except (ItemsNotEnoughError, ItemAlreadyAdded) as ex:
        raise HTTPException(status_code=409, detail=str(ex))

    payload: AddToCartRequest = AddToCartRequest(
        item_id=new_cart_item.item_id, quantity=new_cart_item.quantity
    )
    return AddToCartResponse(items=[payload])


@user_router.get("/{user_id}/cart")
async def get_cart(
    user_id: UUID, repo: Repository = Depends(get_repo)
) -> AddToCartResponse:
    cart_items: List[CartItem] = list_items_in_cart(user_id, repo)

    cart_items_payloads: List[AddToCartRequest] = []
    for cart_item in cart_items or []:
        cart_items_payloads.append(
            AddToCartRequest(item_id=cart_item.item_id, quantity=cart_item.quantity)
        )

    return AddToCartResponse(items=cart_items_payloads)
