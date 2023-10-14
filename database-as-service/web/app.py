from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
import bcrypt

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        users.insert_one(
            {"Username": username, "Password": hashed_pw, "Sentence": "", "Token": 6}
        )

        retJson = {
            "status": 200,
            "message": "You have successfully signed up for the API",
        }

        return jsonify(retJson)


def verifyPw(username, password):
    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.hashpw(password.encode("utf8"), hashed_pw) == hashed_pw:
        return True
    else:
        return False


def countTokens(username):
    tokens = users.find({"Username": username})[0]["Token"]
    return tokens


class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {"status": 302}
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {"status": 301}
            return jsonify(retJson)

        users.update_one(
            {"Username": username},
            {"$set": {"Sentence": sentence, "Token": num_tokens - 1}},
        )

        retJson = {"status": 200, "message": "Sentence save successfully!"}
        return jsonify(retJson)


class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {"status": 302}
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson = {"status": 301}
            return jsonify(retJson)

        sentence = users.find({"Username": username})[0]["Sentence"]

        users.update_one(
            {"Username": username},
            {"$set": {"Token": num_tokens - 1}},
        )

        retJson = {"status": 200, "sentence": sentence}

        return jsonify(retJson)


api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")

if __name__ == "__main__":
    app.run(host="0.0.0.0")