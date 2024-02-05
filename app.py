# Import the libraries
import pickle
import numpy as np
from nltk.collocations import *
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from fastapi import FastAPI, Request, HTTPException
from transformers import pipeline
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os

import textstat

from textblob import TextBlob

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
nltk.download('punkt')


# Create a FastAPI app
app = FastAPI()
def dummy_fn(x): return x


# Retrieve MongoDB credentials and database info
MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "root")
MONGO_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "example")
MONGO_HOST = "mongo"
MONGO_PORT = "27017"
MONGO_DB = "mydatabase"


MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db['mycollection']


class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        try:
            return super().find_class(__name__, name)
        except AttributeError:
            return super().find_class(module, name)


class InputData(BaseModel):
    prompt: str

# Create a class for the output data


class OutputData(BaseModel):
    response: str


class Model():  # Note "Model" represents the Big 5 OCEAN Model. I can't rename as it seems to affect the pickled files
    def __init__(self):
        self.rfr = RandomForestRegressor(bootstrap=True,
                                         max_features='sqrt',
                                         min_samples_leaf=1,
                                         min_samples_split=2,
                                         n_estimators=200)
        self.rfc = RandomForestClassifier(
            max_features='sqrt', n_estimators=110)
        self.tfidf = TfidfVectorizer(
            stop_words='english', strip_accents='ascii')

    def fit(self, X, y, regression=True):
        X = self.tfidf.fit_transform(X)
        if regression:
            self.rfr = self.rfr.fit(X, y)
        else:
            self.rfc = self.rfc.fit(X, y)

    def predict(self, X, regression=True):
        X = self.tfidf.transform(X)
        if regression:
            return self.rfr.predict(X)
        else:
            return self.rfc.predict(X)

    def predict_proba(self, X, regression=False):
        X = self.tfidf.transform(X)
        if regression:
            raise ValueError('Cannot predict probabilites of a regression!')
        else:
            return self.rfc.predict_proba(X)


# check if the models folder has content in it otherwise install the model
if len(os.listdir('./models/')) == 0:

    pipe = pipeline("text-generation", model="gpt2")
    pipe.save_pretrained("./models/")


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


@app.post("/predict")
def predict(request: Request, input_data: InputData):
    cv = CustomUnpickler(open('MTBIModels/cv.pickle', 'rb')).load()

    idf_transformer = CustomUnpickler(
        open('MTBIModels/idf_transformer.pickle', 'rb')).load()

    lr_ie = CustomUnpickler(
        open('MTBIModels/LR_clf_IE_kaggle.pickle', 'rb')).load()
    lr_jp = CustomUnpickler(
        open('MTBIModels/LR_clf_JP_kaggle.pickle', 'rb')).load()
    lr_ns = CustomUnpickler(
        open('MTBIModels/LR_clf_NS_kaggle.pickle', 'rb')).load()
    lr_tf = CustomUnpickler(
        open('MTBIModels/LR_clf_TF_kaggle.pickle', 'rb')).load()

    # render

    c = cv.transform(word_tokenize(input_data.prompt))
    x = idf_transformer.transform(c)

    ie = lr_ie.predict_proba(x).flatten()
    ns = lr_ns.predict_proba(x).flatten()
    tf = lr_tf.predict_proba(x).flatten()
    jp = lr_jp.predict_proba(x).flatten()

    probs = np.vstack([ie, ns, tf, jp])

    #         names = ["Introversion - Extroversion", "Intuiting - Sensing", "Thinking - Feeling", "Judging - Perceiving"]
    #         for i, dim in enumerate(names):
    #             print(f"{dim:28s}: {probs[i,1]:.3f} - {probs[i, 0]:.3f}")

    Extraversion = probs[0][0]
    Introversion = probs[0][1]
    Sensing = probs[1][0]
    Intuiting = probs[1][1]
    Feeling = probs[2][0]
    Thinking = probs[2][1]
    Perceiving = probs[3][0]
    Judging = probs[3][1]

    if Introversion >= 0.5:
        IE = "I"
    else:
        IE = "E"
    if Intuiting >= 0.5:
        NS = "N"
    else:
        NS = "S"
    if Thinking >= 0.5:
        TF = "T"
    else:
        TF = "F"
    if Judging >= 0.5:
        JP = "J"
    else:
        JP = "P"

    MTBI_Results = [IE+NS+TF+JP, Introversion, Intuiting, Thinking, Judging]

    model = Model()
    models = {}
    models['OPN'] = CustomUnpickler(
        open('BigFiveModels/OPN_model.pkl', 'rb')).load()
    models['CON'] = CustomUnpickler(
        open('BigFiveModels/CON_model.pkl', 'rb')).load()
    models['EXT'] = CustomUnpickler(
        open('BigFiveModels/CON_model.pkl', 'rb')).load()
    models['AGR'] = CustomUnpickler(
        open('BigFiveModels/AGR_model.pkl', 'rb')).load()
    models['NEU'] = CustomUnpickler(
        open('BigFiveModels/NEU_model.pkl', 'rb')).load()
    # analysis OCEAN
    predictions = {}
    trait_list = ['OPN', 'CON', 'EXT', 'AGR', 'NEU']
    X = [input_data.prompt]

    for trait in trait_list:
        pkl_model = models[trait]

        trait_scores = pkl_model.predict(X, regression=True).reshape(1, -1)

        predictions['pred_s'+trait] = trait_scores.flatten()[0]

        trait_categories = pkl_model.predict(X, regression=False)
        predictions['pred_c'+trait] = str(trait_categories[0])

        trait_categories_probs = pkl_model.predict_proba(X)
        predictions['pred_prob_c'+trait] = trait_categories_probs[:, 1][0]
        OCEAN_Analysis = predictions

    # textstat values
    textstat.flesch_reading_ease(input_data.prompt)
    textstat.flesch_kincaid_grade(input_data.prompt)
    textstat.smog_index(input_data.prompt)
    textstat.coleman_liau_index(input_data.prompt)
    textstat.automated_readability_index(input_data.prompt)
    textstat.dale_chall_readability_score(input_data.prompt)
    textstat.difficult_words(input_data.prompt)
    textstat.linsear_write_formula(input_data.prompt)
    textstat.gunning_fog(input_data.prompt)
    textstat.text_standard(input_data.prompt)
    textstat.fernandez_huerta(input_data.prompt)
    textstat.szigriszt_pazos(input_data.prompt)
    textstat.gutierrez_polini(input_data.prompt)
    textstat.crawford(input_data.prompt)
    textstat.gulpease_index(input_data.prompt)
    textstat.osman(input_data.prompt)

    # textblob sentiment analysis
    blob = TextBlob(input_data.prompt)
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
    #  ('threat', 'NN'), ('of', 'IN'), ...]

    blob.noun_phrases   # WordList(['titular threat', 'blob',
    #            'ultimate movie monster',
    #            'amoeba-like mass', ...])

    # Store sentiment polarities in a list
    sentiment_polarities = [
        sentence.sentiment.polarity for sentence in blob.sentences]

    output_dict = {
        "sentiment_polarities": sentiment_polarities,
        "flesch_reading_ease": textstat.flesch_reading_ease(input_data.prompt),
        "MTBI_Results": MTBI_Results,
        "OCEAN_Analysis": OCEAN_Analysis
    }

    return output_dict


@app.post("/insert-record/")
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
