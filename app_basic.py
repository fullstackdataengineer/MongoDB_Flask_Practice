from flask import Flask, jsonify, render_template
import pymongo
import os
import urllib.parse

host=os.environ.get("host")
port=os.environ.get("port")
database=os.environ.get("database")
username=os.environ.get("username")
password=os.environ.get("password")
flaskport=os.environ.get("flaskport")
authentication_database='admin'

client = pymongo.MongoClient('mongodb://{username}:{password}@{host}:{port}/{authentication_database}?retryWrites=true&w=majority'.format(
  username=urllib.parse.quote_plus(username), password=urllib.parse.quote_plus(password), host=host, port=port, authentication_database=authentication_database)) # establish connection with database

mongo_db=client.get_database(database) # assign database to mongo_db

app=Flask(__name__)

# @app.route('/')
# def index(): 
#   return 'Use /all_launches_timeline'

@app.route('/')
def dashboard(): 
    return render_template('index.html')

@app.route('/sample_launch/', strict_slashes=False)
def sample():
    results=mongo_db.launches.find_one({}, {'_id': 0})
    return jsonify(results)

@app.route('/all_launches_timeline/', strict_slashes=False)
def all_launches_timeline(): 
    results=mongo_db.launches.aggregate([
    {'$group': {'_id': {'year': {'$substr': ['$date_utc', 0, 4]},
              'quarter': {'$ceil': {'$divide': [{'$toInt': {'$substr': ['$date_utc', 5, 2]}}, 3]}}},
          'launches': {'$push': {'mission_patch_small': '$links.patch.small', 
                       'mission_name': '$name', 
                       'video_link': '$links.webcast', 
                       'wikipedia': '$links.wikipedia', 
                       'mission_patch': '$links.patch.large'}}}}])
    return jsonify(list(results))

if __name__=='__main__': 
    app.run(port=flaskport)