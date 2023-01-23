from contextlib import asynccontextmanager
from typing import Iterable, List, Any

import aiomysql

from utils.tools.singletonType import SingletonType
from utils.tools.configManager import ConfigReader, BASE_DIR

__all__ = ['SqlManager']


class SqlManager(metaclass=SingletonType):
    def __init__(self):
        # self.connect_args = (str(BASE_DIR) + ConfigReader().get_config('DatabaseConfig', 'path'),)
        self.connect_args = {
            'host': ConfigReader().get_config('DatabaseConfig', 'host'),
            'port': ConfigReader().get_config('DatabaseConfig', 'port'),
            'user': ConfigReader().get_config('DatabaseConfig', 'user'),
            'password': ConfigReader().get_config('DatabaseConfig', 'password'),
        }

    @asynccontextmanager
    async def connect(self) -> aiomysql.Connection:
        async with aiomysql.connect(**self.connect_args) as db:
            try:
                yield db
            except aiomysql.OperationalError as e:
                await db.rollback()
            finally:
                await db.commit()

    @asynccontextmanager
    async def execute(self, sql: str, parameters: Iterable[Any] = None) -> aiomysql.Cursor:
        async with self.connect() as db:
            async with db.execute(sql, parameters) as cursor:
                yield cursor

    @asynccontextmanager
    async def executemany(self, sql: str, parameters: Iterable[Iterable[Any]]) -> aiomysql.Cursor:
        async with self.connect() as db:
            async with db.executemany(sql, parameters) as cursor:
                yield cursor
