from pydantic import BaseModel, Field
from typing import List


class HealthItem(BaseModel):
    """
    Model For Alive Check
    """
    alive: bool = Field(default=False)
    db_healthy: bool = Field(default=False)
    timestamp: float
    