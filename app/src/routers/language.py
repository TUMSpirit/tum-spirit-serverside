from fastapi import APIRouter

from ..language_helpers.analyze_chat import analyze_chat
from ..language_helpers.api.sentiment import get_sentiment

from datetime import datetime

from bson import ObjectId

router = APIRouter()

@router.get("/language/analyze", tags=["language"])
def predict():    
    return analyze_chat()


@router.get("/language/hello", tags=["language"])
def hello_world():

    return {"message": "Hello World"}


@router.get("/language/sentiment", tags=["language"])
def sentiment(startDate:datetime=None, endDate:datetime=None):
    return get_sentiment(ObjectId("663506d86905198ad715ded8"), startDate, endDate)