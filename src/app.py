from flask import Flask, request, jsonify, Response
from flask_pymongo import pymongo
from bson import json_util
from bson.objectid import ObjectId

# Create server from Flask
app = Flask(__name__)

CONNECTION_STRING = "mongodb+srv://curn:parcialpython@parcial.hsbxr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# Config database
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')

# create new user
@app.route('/user', methods=['POST'])
def createUser():
    data = request.json
    user_collection.insert(data)
    return { "message": "Data saved successfully" }

# get all users
@app.route('/users', methods=['GET'])
def getUser():
    data = user_collection.find({})
    response = json_util.dumps(data)
    return Response(response, mimetype='application/json')

# get user from id param
@app.route('/user/<id>', methods=['GET'])
def getUserFromId(id):
    data = user_collection.find_one({ "_id": ObjectId(id) })
    response = json_util.dumps(data)
    return Response(response, mimetype='application/json')

# delete user from id param
@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    user_collection.delete_one({ "_id": ObjectId(id) })
    return jsonify({ "message": "User deleted succcesfully" })

# update user from id param
@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    body = request.json
    user_collection.update_one({ "_id": ObjectId(id) }, { '$set': {
        "name": body["name"],
        "role": body["role"],
    }})
    return jsonify({ "message": "User updated succcesfully" })

# Run server
if __name__ == '__main__':
    app.run(debug=True, port=4000)