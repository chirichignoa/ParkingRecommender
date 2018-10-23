import pickle

from flask import Flask, jsonify, request, make_response
from pathlib import Path
from util.predictor import dump_model

app = Flask(__name__)

model = None


@app.before_first_request
def startup():
    global model
    my_file = Path("../models/model.pkl")
    if not my_file.is_file():
        dump_model()
    model = pickle.load(open("../models/model.pkl", "rb"))
    if model is not None:
        print("Model loaded!")
    else:
        print("Model not loaded!")


@app.route("/")
def first_page():
    return jsonify("Parking Recommender")


@app.route('/predict', methods=['POST'])
def predict():
    feature_array = request.get_json()['feature_array']
    if (feature_array is None) or (feature_array == ""):
        resp = make_response("The request does not have the necessary parameters", 200)
        return resp

    prediction = model.predict([feature_array]).tolist()
    return make_response(jsonify({'prediction': prediction}), 200)


@app.errorhandler(400)
def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp
