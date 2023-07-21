import os
from logging import Logger, getLogger
from typing import Any, AsyncGenerator, Final, List

from psycopg import AsyncConnection, AsyncCursor


class DatabaseClient(object):
    logger: Final[Logger] = getLogger(__name__)

    def __init__(self):
        self.__postgres_user = os.environ["POSTGRES_USER"]
        self.__postgres_password = os.environ["POSTGRES_PASSWORD"]
        self.__postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgres_db = os.environ["POSTGRES_DB"]
        self.__postgres_host = os.environ["POSTGRES_HOST"]
        self.__connection_string = f"host={self.__postgres_host} port={self.__postgres_port} dbname={self.__postgres_db} user={self.__postgres_user} password={self.__postgres_password}"

    async def select_as_super_user(
        self,
        query: str,
    ) -> List[Any]:
        async with await AsyncConnection.connect(conninfo=self.__connection_string) as connection:
            async with connection.cursor() as cursor:
                try:
                    await cursor.execute(query=query)
                    return await cursor.fetchall()
                except Exception as e:
                    self.logger.error(f"query by super user failed for {e}")
                    raise e

    async def select(
        self,
        tenant_id: int,
        query: str,
    ) -> List[Any]:
        async with await AsyncConnection.connect(conninfo=self.__connection_string) as connection:
            async with connection.cursor() as cursor:
                try:
                    set_tenant = f"SET app.current_tenant={tenant_id};"
                    self.logger.info(f"set_tenant={set_tenant}")
                    await cursor.execute(query=set_tenant)
                    await cursor.execute(query=query)
                    return await cursor.fetchall()
                except Exception as e:
                    self.logger.error(f"query failed for {e}")
                    raise e

    async def insert(
        self,
        tenant_id: int,
        query: str,
    ):
        async with await AsyncConnection.connect(conninfo=self.__connection_string) as connection:
            async with connection.cursor() as cursor:
                try:
                    set_tenant = f"SET app.current_tenant={tenant_id};"
                    self.logger.info(f"set_tenant={set_tenant}")
                    await cursor.execute(query=set_tenant)
                    await cursor.execute(query=query)
                    await connection.commit()
                except Exception as e:
                    self.logger.error(f"query failed for {e}")
                    await connection.rollback()
                    raise e
