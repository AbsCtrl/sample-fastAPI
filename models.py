from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class HealthItem(BaseModel):
    """
    Model For Alive Check
    """

    alive: bool = Field(default=False)
    db_healthy: bool = Field(default=False)
    timestamp: float


class NameItem(BaseModel):
    """
    Object only containing user's full name
    """

    name: str = Field(required=True)


class CommentObject(BaseModel):
    """
    A single comment
    """

    name: str
    email: str
    text: str
    date: Optional[datetime] = None


class CommentList(BaseModel):
    """
    List of Comment Objects
    """
    
    comments: List[CommentObject]