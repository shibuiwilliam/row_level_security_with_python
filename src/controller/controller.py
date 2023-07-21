from logging import Logger, getLogger
from typing import Final, List, Optional

from fastapi import APIRouter

from src.infrastructure.database import DatabaseClient
from src.model.app_user import AppUser
from src.model.log import Log
from src.model.tenant import Tenant
from src.service.app_user_service import AppUserService
from src.service.health_check_service import HealthCheck, HealthCheckService
from src.service.log_service import LogService
from src.service.tenant_service import TenantService

logger: Final[Logger] = getLogger(__name__)

database_client: Final[DatabaseClient] = DatabaseClient()


health_check_router = APIRouter()
health_check_service: Final[HealthCheckService] = HealthCheckService()


@health_check_router.get(
    path="",
    response_model=HealthCheck,
)
async def health_check() -> HealthCheck:
    return await health_check_service.health_check()


tenant_router = APIRouter()
tenant_service: Final[TenantService] = TenantService(
    database_client=database_client,
)


@tenant_router.get(
    path="",
    response_model=Optional[Tenant],
)
async def get_tenant(name: str) -> Optional[Tenant]:
    logger.info(f"request get_tenant name={name}")
    return await tenant_service.get_tenant(name=name)


app_user_router = APIRouter()
app_user_service: Final[AppUserService] = AppUserService(
    database_client=database_client,
)


@app_user_router.get(
    path="",
    response_model=List[AppUser],
)
async def get_app_users(tenant_id: int) -> List[AppUser]:
    logger.info(f"request get_app_user tenant_id={tenant_id}")
    return await app_user_service.get_app_users(
        tenant_id=tenant_id,
    )


log_router = APIRouter()
log_service: Final[LogService] = LogService(
    database_client=database_client,
)


@log_router.get(
    path="",
    response_model=List[Log],
)
async def get_logs(tenant_id: int) -> List[Log]:
    logger.info(f"request get_logs tenant_id={tenant_id}")
    return await log_service.get_logs(
        tenant_id=tenant_id,
    )


@log_router.post(
    path="",
)
async def add_log(tenant_id: int) -> None:
    logger.info(f"request add_log tenant_id={tenant_id}")
    await log_service.add_log(
        tenant_id=tenant_id,
    )
