from logging import Logger, getLogger
from typing import Final, Optional

from src.infrastructure.database import DatabaseClient
from src.model.table import Table
from src.model.tenant import Tenant


class TenantService(object):
    logger: Final[Logger] = getLogger(__name__)

    def __init__(
        self,
        database_client: DatabaseClient,
    ):
        self.__database_client = database_client

    async def get_tenant(
        self,
        name: str,
    ) -> Optional[Tenant]:
        self.logger.info(f"request get_tenant name={name}")
        query = f"""SELECT 
    id, 
    name, 
    created_at 
FROM 
    {Table.TENANT.value} 
WHERE 
    name = '{name}';"""
        self.logger.info(f"query={query}")
        rows = await self.__database_client.select_as_super_user(query=query)
        self.logger.info(f"row={rows}")
        if len(rows) == 0:
            self.logger.info(f"tenant not found")
            return None
        tenant = Tenant.from_tuple(rows[0])
        self.logger.info(f"tenant={tenant}")
        return tenant
