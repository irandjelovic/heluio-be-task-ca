import abc
from typing import List
from uuid import UUID

from be_task_ca.item.entities import Item


class Repository(abc.ABC):
    @abc.abstractmethod
    def save_item(self, item: Item) -> Item:
        pass

    @abc.abstractmethod
    def get_all_items(self) -> List[Item]:
        pass

    @abc.abstractmethod
    def find_item_by_name(self, name: str) -> Item | None:
        pass

    @abc.abstractmethod
    def find_item_by_id(self, id: UUID) -> Item | None:
        pass
