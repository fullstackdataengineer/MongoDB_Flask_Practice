import os
import json
import urllib.parse
import pymongo

host=os.environ.get("host")
port=os.environ.get("port")
database=os.environ.get("database")
username=os.environ.get("username")
password=os.environ.get("password")
authentication_database='admin'

launches='static/data/launches.json' # assume that another process keeps on updating launches.json from another process

client = pymongo.MongoClient('mongodb://{username}:{password}@{host}:{port}/{authentication_database}?retryWrites=true&w=majority'.format(
  username=urllib.parse.quote_plus(username), password=urllib.parse.quote_plus(password), host=host, port=port, authentication_database=authentication_database)) # establish connection with database

mongo_db=client.get_database(database) # assign database to mongo_db
mongo_db.launches.drop() # clear the collection

with open(launches) as file: # opening the json file
    file_data = json.load(file)

if isinstance(file_data, list):
    mongo_db.launches.insert_many(file_data) # if data is a list
else:
    mongo_db.launches.insert_one(file_data) # if data is a document object

print(f"Dataset {launches} successfully loaded into mongodb://{host}:{port}/{database}!")