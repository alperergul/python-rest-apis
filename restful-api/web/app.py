from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update_one({}, {"$set": {"num_of_users": new_num}})
        return str("Hello user " + str(new_num))
    
class Reset(Resource):
    def get(self):
        UserNum.update_one({}, {"$set": {"num_of_users": 0}})
        return str("Success!")

def checkPostedData(postedData, functionName):
    if(functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
    elif functionName == "division":
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif(int( postedData["y"]) == 0 ):
            return 302
        else:
            return 200

class Add(Resource):

    def post(self):
        postedData = request.get_json()
        statusCode = checkPostedData(postedData, "add")

        if statusCode != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code": statusCode
            }

            return jsonify(retJson)

        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)
        ret = x+y

        retMap = {
            "Message": ret,
            "Status Code": statusCode
        }

        return jsonify(retMap)

class Subtract(Resource):
    def post(self):

        postedData = request.get_json()

        statusCode = checkPostedData(postedData, "subtract")

        if statusCode != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code": statusCode
            }

            return jsonify(retJson)

        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)
        ret = x-y

        retMap = {
            "Message": ret,
            "Status Code": statusCode
        }

        return jsonify(retMap)

class Multiply(Resource):
    def post(self):

        postedData = request.get_json()

        statusCode = checkPostedData(postedData, "multiply")

        if statusCode != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code": statusCode
            }

            return jsonify(retJson)

        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)
        ret = x*y

        retMap = {
            "Message": ret,
            "Status Code": statusCode
        }

        return jsonify(retMap) 

class Divide(Resource):
    def post(self):

        postedData = request.get_json()

        statusCode = checkPostedData(postedData, "division")

        if statusCode != 200:
            retJson = {
                "Message": "An error happened",
                "Status Code": statusCode
            }

            return jsonify(retJson)

        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)
        ret = (x*1.0)/y

        retMap = {
            "Message": ret,
            "Status Code": statusCode
        }

        return jsonify(retMap) 

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit, "/hello")
api.add_resource(Reset, "/reset")


@app.route('/')
def hello_world():
    return "Hello World!"

if __name__=="__main__":
    app.run(host='0.0.0.0')


