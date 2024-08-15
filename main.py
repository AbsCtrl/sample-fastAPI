import logging
import time
from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.database import Database
from fastapi.responses import JSONResponse

from constants import LOG_LEVEL
from metadata import title, description, version, contact, tags_metadata
from models import HealthItem, NameItem, CommentList, CommentObject
from utils import check_database_health, connect_to_mongodb

# Configure Logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# FastAPI Setup
app = FastAPI(
    title=title,
    description=description,
    version=version,
    contact=contact,
    openapi_tags=tags_metadata,
)

# Configuring CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint Functions
@app.get("/", tags=["health"])
def alive_check(database_health: bool = Depends(check_database_health)) -> HealthItem:
    """
    Health Check Endpoint that verifies the health of the API and the MongoDB Database connection

    Args:
    - database_health (bool): Result of the database health check

    Returns:
    - HealthItem: Response indicating the health status of the API and the database
    """
    return HealthItem(alive=True, db_healthy=database_health, timestamp=time.time())


@app.get("/getUserComments/{name}", tags=["comments"])
async def get_all_comments_by_user(
    name: str, db: Database = Depends(connect_to_mongodb)
) -> CommentList:
    """
    Endpoint that returns all comments by a certain user

    Args:
    - name (String): The name of the user

    Returns:
    - commentList (CommentList): List of all comments left by the user
    """

    query = {"name": name}

    resultsList = list(db.comments.find(query))
    commentsList = {"comments": resultsList}
    return commentsList


@app.post("/addNewComment", tags=["comments"])
async def add_new_comment(
    new_comment: CommentObject, db: Database = Depends(connect_to_mongodb)
):
    """
    Endpoint that adds a comment object

    Args:
    - new_comment (CommentObject): A comment left by the user

    Returns:
    - http Response
    """
    commentDoc = {
        "name": new_comment.name,
        "email": new_comment.email,
        "text": new_comment.text,
        "date": new_comment.date if new_comment.date else datetime.now(),
    }

    result = db.comments.insert_one(commentDoc)
    return JSONResponse(status_code=201, content={"success": result.acknowledged})
