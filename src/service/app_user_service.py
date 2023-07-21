from logging import Logger, getLogger
from typing import Final, List, Optional

from src.infrastructure.database import DatabaseClient
from src.model.app_user import AppUser
from src.model.table import Table


class AppUserService(object):
    logger: Final[Logger] = getLogger(__name__)

    def __init__(
        self,
        database_client: DatabaseClient,
    ):
        self.__database_client = database_client

    async def get_app_users(
        self,
        tenant_id: int,
    ) -> List[AppUser]:
        self.logger.info(f"request get_app_users tenant_id={tenant_id}")
        query = f"""SELECT 
    id, 
    tenant_id, 
    name, 
    created_at 
FROM 
    {Table.APP_USER.value} ;"""
        self.logger.info(f"query={query}")
        rows = await self.__database_client.select(
            tenant_id=tenant_id,
            query=query,
        )
        self.logger.info(f"row={rows}")
        app_users = [AppUser.from_tuple(r) for r in rows]
        self.logger.info(f"app_users={app_users}")
        return app_users
