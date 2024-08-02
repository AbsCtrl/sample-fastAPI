from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from fastapi import Depends

from constants import DB_URI


def connect_to_mongodb(database_uri=DB_URI, timeout=2) -> Database:
    """
    connect to mongoDB database

    args:
    - database_uri (str): mongoDB connection URI default is taken from .env via constants
    - timeout (int): timeout for connection in seconds, default is 2 seconds

    yields:
    - pymongo.database.Database: mongoDB Database object
    """
    client = None
    try:
        client = MongoClient(database_uri, serverSelectionTimeoutMS=int(timeout) * 1000)
        db = client.get_default_database()
        yield db
    except Exception as e:
        # raise because we don't know what we're handling
        raise e
    else:
        client.close()


def check_database_health(db: MongoClient = Depends(connect_to_mongodb)):
    """
    Check the health of the MongoDB database connection

    returns:
    - bool: True if the database connection is healthy
            False otherwise
    """
    try:
        # attempt to run a simple query to check if the connection is healthy
        db.list_collection_names()
        return True
    except ServerSelectionTimeoutError:
        return False
