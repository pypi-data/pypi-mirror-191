from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class NomadAllocation(BaseModel):
    id: Optional[str] = Field(default_factory=str)
    id_long: Optional[str] = Field(default_factory=str)
