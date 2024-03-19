from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from fastapi import Request
from typing import List, Optional


class Message(BaseModel):
    role: str
    content: str


class MessageList(BaseModel):
    messages: List[Message]


router = APIRouter()


# Retrieve MongoDB credentials and database info
MONGO_USER = "root"
MONGO_PASSWORD = "example"
MONGO_HOST = "mongo"
MONGO_PORT = "27017"
MONGO_DB = "TUMSpirit"


MONGO_URI = "mongodb://root:example@localhost:27017"


@router.post("/ai/generate", tags=["ai"])
def generate(messages: MessageList):

    client = OpenAI(
        base_url='http://172.17.0.1:54321/v1',
        api_key='ollama',  # required, but unused
    )

    response = client.chat.completions.create(
        model="llama2",
        messages=messages.messages
    )
    print(response.choices[0].message.content)

    return response


@router.get("/ai/hello", tags=["ai"])
def generate():

    return {"message": "Hello World"}


@router.post("/insert-record/")
def insert_record():
    try:
        # Create a record with a random ID (ObjectId) and a timestamp
        record = {
            '_id': ObjectId(),
            'timestamp': datetime.utcnow()
        }
        # Inserting the record into the database
        result = collection.insert_one(record)
        # Return the ID of the inserted record
        return {"id": str(result.inserted_id)}
    except Exception as e:
        # If something goes wrong, raise an HTTP exception
        raise HTTPException(status_code=500, detail=str(e))
