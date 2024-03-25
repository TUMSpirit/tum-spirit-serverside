# Import necessary libraries
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from bson import ObjectId
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import os


# Load environment variables from a .env file
load_dotenv()

# Define a BaseModel for representing a single message


class Message(BaseModel):
    role: str  # Defines the role of the sender (e.g., user, bot)
    content: str  # The actual message content


# Define a BaseModel for representing a list of messages
class MessageList(BaseModel):
    messages: List[Message]  # A list of Message objects


# Create a FastAPI router object
router = APIRouter()


# Access environment variables for database credentials
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
# Add an environment variable for OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Construct the MongoDB connection URI
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"


# Endpoint to generate AI responses using OpenAI
@router.post("/ai/generate", tags=["ai"])
async def generate(messages: MessageList):

    # Initialize OpenAI client
    client = OpenAI(
        base_url='http://127.0.0.1:11434/v1',
        api_key=OPENAI_API_KEY,
    )

    # Prepare the request data using the provided messages
    response = client.chat.completions.create(
        model="llama2",
        messages=messages.messages
    )

    # Print the generated response for debugging purposes (remove for production)
    print(response.choices[0].message.content)

    # Return the OpenAI response object
    return response


# Simple endpoint to return a "Hello World" message
@router.get("/ai/hello", tags=["ai"])
async def generate():

    return {"message": "Hello World"}


# Endpoint to insert a record into the MongoDB database (**WARNING:** Not implemented)
@router.post("/insert-record/")
async def insert_record():
    try:
        # This functionality is currently not implemented
        # Replace this with your actual logic for connecting to MongoDB and inserting records
        raise NotImplementedError("Database functionality not implemented yet")

    except Exception as e:
        # Handle any exceptions that might occur during database operations
        raise HTTPException(status_code=500, detail=str(e))
