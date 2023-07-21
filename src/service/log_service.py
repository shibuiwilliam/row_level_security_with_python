import random
import string
from logging import Logger, getLogger
from typing import Final, List, Optional

from src.infrastructure.database import DatabaseClient
from src.model.log import Log
from src.model.table import Table


def random_str(n: int) -> str:
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


class LogService(object):
    logger: Final[Logger] = getLogger(__name__)

    def __init__(
        self,
        database_client: DatabaseClient,
    ):
        self.__database_client = database_client

    async def get_logs(
        self,
        tenant_id: int,
    ) -> List[Log]:
        self.logger.info(f"request get_logs tenant_id={tenant_id}")
        query = f"""SELECT 
    id, 
    tenant_id, 
    log, 
    created_at 
FROM 
    {Table.LOG.value} ;"""
        self.logger.info(f"query={query}")
        rows = await self.__database_client.select(
            tenant_id=tenant_id,
            query=query,
        )
        self.logger.info(f"row={rows}")
        logs = [Log.from_tuple(r) for r in rows]
        self.logger.info(f"logs={logs}")
        return logs

    async def add_log(
        self,
        tenant_id: int,
    ):
        log = random_str(n=10)
        self.logger.info(f"request add_log tenant_id={tenant_id} log={log}")
        query = f"""INSERT INTO {Table.LOG.value} 
(tenant_id, log) 
VALUES ({tenant_id}, '{log}');"""
        self.logger.info(f"query={query}")
        await self.__database_client.insert(
            tenant_id=tenant_id,
            query=query,
        )
        self.logger.info(f"add_log success")
