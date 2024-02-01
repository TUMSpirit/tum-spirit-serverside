# Import the libraries
from fastapi import FastAPI, Request
from transformers import pipeline
from pydantic import BaseModel

# Create a FastAPI app
app = FastAPI()

# Create a class for the input data


class InputData(BaseModel):
    prompt: str

# Create a class for the output data


class OutputData(BaseModel):
    response: str


# Load a local LLM using Hugging Face Transformers
model = pipeline("text-generation", model="./models/")

# Create a route for the web application


@app.post("/generate", response_model=OutputData)
def generate(request: Request, input_data: InputData):
    # Get the prompt from the input data
    prompt = input_data.prompt

# Generate a response from the local LLM using the prompt
    response = model(prompt)[0]["generated_text"]

# Return the response as output data
    return OutputData(response=response)


@app.get("/")
def home():
    return {"message": "Hello World"}
