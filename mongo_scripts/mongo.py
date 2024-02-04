from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import find_dotenv, load_dotenv
from os import environ as env

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

uri = f"mongodb+srv://arnet:{env.get('MONGO_PW')}@cluser0.i7wnmup.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.resumate
resumes = db.resumes

resumesDocument = {
    "user" : 1,
}

resumes.insert_one(resumesDocument)


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)