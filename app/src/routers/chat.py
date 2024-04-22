from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException


# Create a router
router = APIRouter()


# Retrieve MongoDB credentials and database info
MONGO_USER = "root"
MONGO_PASSWORD = "example"
MONGO_HOST = "mongo"
MONGO_PORT = "27017"
MONGO_DB = "TUMSpirit"

# connection string
MONGO_URI = "mongodb://root:example@129.187.135.9:27017/mydatabase?authSource=admin"


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db['chat']


# Define a route to insert a record into the database
@router.get("/chat/hello", tags=["chat"])
async def generate():

    return {"message": "Hello World"}