from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


@app.route("/hitthere")
def hit():
    return "just hit there"


@app.route("/add_two_nums", methods=["POST"])
def add_two_nums():
    dataDict = request.get_json()

    if "y" not in dataDict:
        return "ERROR", 305

    x = dataDict["x"]
    y = dataDict["y"]
    z = x + y

    retJson = {"z": z}

    return jsonify(retJson), 200


@app.route("/bye")
def bye():
    age = 2 * 5

    retJson = {
        "Name": "Alper",
        "Age": age,
        "phones": [
            {
                "phoneName": "Iphone8",
                "phoneNumber": 123213,
            },
            {
                "phoneName": "Nokia",
                "phoneNumber": 123213,
            },
        ],
    }

    return jsonify(retJson), 200


if __name__ == "__main__":
    app.run(debug=True)
