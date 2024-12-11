import logging

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

Base = declarative_base()


class DbConnection:
    _instance: "DbConnection" = None
    _engine: Engine = None
    _session_factory = None
    _session: Session

    def __init__(self, db_url: str):
        if self._engine is None:
            self._engine = create_engine(url=db_url)
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def engine(self):
        return self._engine

    def __enter__(self):
        self._session = self.get_session()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def get_session(self) -> Session:
        return self._session_factory()
