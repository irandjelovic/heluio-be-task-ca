from uuid import UUID

from be_task_ca.item.api import get_repo
from be_task_ca.item.entities import Item
from be_task_ca.item.model import ItemDB
from be_task_ca.item.repository.repository import Repository


def item_foreign_key():
    return ItemDB.id


def find_item_by_id(id: UUID) -> Item:
    repo: Repository = get_repo()
    return repo.find_item_by_id(id)
