import asyncio
import random
from logging import Logger
from typing import Final

from src.infrastructure.database import DatabaseClient
from src.middleware.logger import get_logger
from src.service.log_service import LogService

logger: Final[Logger] = get_logger(name=__name__)
database_client: Final[DatabaseClient] = DatabaseClient()
log_service: Final[LogService] = LogService(
    database_client=database_client,
)


async def read_logs(tenant_id: int):
    logs = await log_service.get_logs(
        tenant_id=tenant_id,
    )
    logger.info(f"logs={logs}")
    for log in logs:
        if log.tenant_id != tenant_id:
            logger.error(f"invalid tenant_id={log.tenant_id}")


async def add_log(tenant_id: int):
    await log_service.add_log(
        tenant_id=tenant_id,
    )


async def main():
    logger.info("START!!!")
    await asyncio.sleep(100)
    while True:
        await asyncio.sleep(10)
        tenant_id = 1 if random.random() < 0.5 else 2
        logger.info(f"start targeting tenant_id={tenant_id}...")
        try:
            await add_log(tenant_id=tenant_id)
            await read_logs(tenant_id=tenant_id)
        except Exception as e:
            logger.error(f"error={e}")
        logger.info(f"...done")


if __name__ == "__main__":
    asyncio.run(main())
