from pymongo import MongoClient

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

def get_db(collection: str):
    return db[collection]