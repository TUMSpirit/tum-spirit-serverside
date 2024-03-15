from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI


class Messages(BaseModel):
    messages: list[str]


router = APIRouter()


@router.get("/ai/generate", tags=["ai"])
def generate(messages: Messages):

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
