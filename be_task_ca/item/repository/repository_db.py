from typing import List
from uuid import UUID

from be_task_ca.database import DbConnection
from be_task_ca.item.entities import Item
from be_task_ca.item.model import ItemDB
from be_task_ca.item.repository.repository import Repository


class RepositoryDb(Repository):
    _conn: DbConnection

    def __init__(self, db_url: str):
        self._conn = DbConnection(db_url=db_url)

    def save_item(self, item: Item) -> Item:
        item_db: ItemDB = ItemDB.from_entity(item)
        with self._conn as session:
            session.add(item_db)
            session.commit()
            return item_db.to_entity()

    def get_all_items(self) -> List[Item]:
        with self._conn as session:
            items: List[ItemDB] = session.query(ItemDB).all()
            return [item.to_entity() for item in items]

    def find_item_by_name(self, name: str) -> Item | None:
        with self._conn as session:
            item: ItemDB = session.query(ItemDB).filter(ItemDB.name == name).first()
            return item.to_entity() if item else None

    def find_item_by_id(self, id: UUID) -> Item | None:
        with self._conn as session:
            item: ItemDB = session.query(ItemDB).filter(ItemDB.id == id).first()
            return item.to_entity() if item else None
