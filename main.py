import logging
import time
from datetime import datetime

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from constants import LOG_LEVEL
from metadata import title, description, version, contact, tags_metadata
from models import HealthItem
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
