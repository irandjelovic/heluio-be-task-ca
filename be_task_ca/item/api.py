from typing import List

from fastapi import APIRouter, Depends, HTTPException

from .entities import Item
from .exceptions import ItemDuplicateError
from .repository.repository import Repository
from .repository.repository_db import RepositoryDb
from .repository.repository_im import RepositoryIM
from .schema import CreateItemRequest, CreateItemResponse, AllItemsResponse
from .usecases import create_item, get_all
from ..settings import settings

item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


def get_repo() -> Repository:
    db: str = settings.tool.project_config.db
    if db == "memory":
        return RepositoryIM()
    return RepositoryDb(db_url=db)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, repo: Repository = Depends(get_repo)
) -> CreateItemResponse:
    item: Item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    try:
        item: Item = create_item(item, repo)
    except ItemDuplicateError as ex:
        raise HTTPException(status_code=409, detail=str(ex))

    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )


@item_router.get("/")
async def get_items(repo: Repository = Depends(get_repo)) -> AllItemsResponse:
    items: List[Item] = get_all(repo)
    item_payloads: List[CreateItemResponse] = [
        CreateItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        for item in items
    ]
    return AllItemsResponse(items=item_payloads)
