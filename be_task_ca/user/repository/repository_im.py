import uuid
from typing import List, Optional
from uuid import UUID

from be_task_ca.user.entities import CartItem, User
from be_task_ca.user.repository.repository import Repository


class RepositoryIM(Repository):
    _users: List[User] = []

    def save_user(self, user: User) -> User:
        user.id = uuid.uuid4()
        self._users.append(user)
        return user

    def find_user_by_email(self, email: str) -> User | None:
        return next((user for user in self._users if user.email == email), None)

    def find_user_by_id(self, user_id: UUID) -> User | None:
        return next((user for user in self._users if user.id == user_id), None)

    def find_cart_items_for_user_id(self, user_id) -> List[CartItem]:
        user: Optional[User] = next((user for user in self._users if user.id == user_id), None)
        return user.cart_items if user else []
