from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Extra


class Log(BaseModel):
    id: UUID
    tenant_id: int
    log: str
    created_at: datetime

    class Config:
        validate_assignment = True
        frozen = True
        allow_mutation = False
        extra = Extra.forbid

    @staticmethod
    def from_tuple(row: tuple) -> "Log":
        return Log(
            id=row[0],
            tenant_id=row[1],
            log=row[2],
            created_at=row[3],
        )
