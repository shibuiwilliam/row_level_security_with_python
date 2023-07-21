from datetime import datetime
from typing import Tuple

from pydantic import BaseModel, Extra


class Tenant(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        validate_assignment = True
        frozen = True
        allow_mutation = False
        extra = Extra.forbid

    @staticmethod
    def from_tuple(row: Tuple[int, str, datetime]) -> "Tenant":
        return Tenant(
            id=row[0],
            name=row[1],
            created_at=row[2],
        )
