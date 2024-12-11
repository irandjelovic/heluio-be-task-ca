import uuid
from typing import List
from uuid import UUID

from be_task_ca.item.entities import Item
from be_task_ca.item.repository.repository import Repository


class RepositoryIM(Repository):
    _items: List[Item] = []

    def save_item(self, item: Item) -> Item:
        item.id = uuid.uuid4()
        self._items.append(item)
        return item

    def get_all_items(self) -> List[Item]:
        return self._items

    def find_item_by_name(self, name: str) -> Item | None:
        return next((item for item in self._items if item.name == name), None)

    def find_item_by_id(self, id: UUID) -> Item | None:
        return next((item for item in self._items if item.id == id), None)
