from typing import List

from .exceptions import ItemDuplicateError
from .model import Item
from .repository.repository import Repository


def create_item(item: Item, repo: Repository) -> Item:
    existing_item: Item = repo.find_item_by_name(item.name)
    if existing_item is not None:
        raise ItemDuplicateError(f"An item with this name already exists: {item.name}")

    return repo.save_item(item)


def get_all(repo: Repository) -> List[Item]:
    return repo.get_all_items()
