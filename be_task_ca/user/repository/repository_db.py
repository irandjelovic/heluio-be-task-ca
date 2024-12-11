from typing import List, Optional
from uuid import UUID

from be_task_ca.database import DbConnection
from be_task_ca.user.entities import CartItem, User
from be_task_ca.user.model import CartItemDB, UserDB
from be_task_ca.user.repository.repository import Repository


class RepositoryDb(Repository):
    _conn: DbConnection

    def __init__(self, db_url: str):
        self._conn = DbConnection(db_url=db_url)

    def save_user(self, user: User) -> User:
        db_user: UserDB = UserDB.from_entity(user)
        with self._conn.get_session() as session:
            session.merge(db_user)
            session.commit()
            return db_user.to_entity()

    def find_user_by_email(self, email: str) -> User | None:
        with self._conn.get_session() as session:
            db_user: Optional[UserDB] = session.query(UserDB).filter(UserDB.email == email).first()
            return db_user.to_entity() if db_user else None

    def find_user_by_id(self, user_id: UUID) -> User | None:
        with self._conn.get_session() as session:
            db_user: Optional[UserDB] = session.query(UserDB).filter(UserDB.id == user_id).first()
            return db_user.to_entity() if db_user else None

    def find_cart_items_for_user_id(self, user_id) -> List[CartItem]:
        with self._conn.get_session() as session:
            cart_items_db: List[CartItemDB] = session.query(CartItemDB).filter(CartItemDB.user_id == user_id).all()
            return [ci.to_entity() for ci in cart_items_db]
