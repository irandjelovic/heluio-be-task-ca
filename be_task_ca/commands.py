from .database import Base, DbConnection
from .settings import settings

# just importing all the models is enough to have them created
# flake8: noqa
from .user.model import UserDB, CartItemDB
from .item.model import ItemDB


def create_db_schema():
    db_url: str = settings.tool.project_config.db
    Base.metadata.create_all(bind=DbConnection(db_url).engine)
