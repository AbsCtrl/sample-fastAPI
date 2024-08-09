from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import objectid

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


class CommentResponse(BaseModel):
    """
    A single comment
    """

    _id: objectid
    name: str
    email: str
    movie_id: objectid
    text: str
    date: datetime


class CommentList(BaseModel):
    """
    List of Comments
    """
    
    comments: List[CommentResponse]