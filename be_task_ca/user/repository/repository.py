import abc
from typing import List
from uuid import UUID

from be_task_ca.user.entities import User, CartItem


class Repository(abc.ABC):
    @abc.abstractmethod
    def save_user(self, user: User) -> User:
        pass

    @abc.abstractmethod
    def find_user_by_email(self, email: str) -> User | None:
        pass

    @abc.abstractmethod
    def find_user_by_id(self, user_id: UUID) -> User | None:
        pass

    @abc.abstractmethod
    def find_cart_items_for_user_id(self, user_id) -> List[CartItem]:
        pass
