from datetime import datetime
from typing import Tuple

from pydantic import BaseModel, Extra


class AppUser(BaseModel):
    id: int
    tenant_id: int
    name: str
    created_at: datetime

    class Config:
        validate_assignment = True
        frozen = True
        allow_mutation = False
        extra = Extra.forbid

    @staticmethod
    def from_tuple(row: Tuple[int, int, str, datetime]) -> "AppUser":
        return AppUser(
            id=row[0],
            tenant_id=row[1],
            name=row[2],
            created_at=row[3],
        )
