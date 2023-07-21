from logging import Logger, getLogger
from typing import Final

from pydantic import BaseModel, Extra


class HealthCheck(BaseModel):
    health_check: str = "ok"

    class Config:
        validate_assignment = True
        frozen = True
        allow_mutation = False
        extra = Extra.forbid


class HealthCheckService(object):
    logger: Final[Logger] = getLogger(__name__)

    def __init__(self):
        pass

    async def health_check(self) -> HealthCheck:
        self.logger.info("health check")
        return HealthCheck()
