import json
import pickle

from flask import Flask, jsonify, request, make_response
from pathlib import Path
from util.predictor import dump_model, get_index
import requests
from flask_cors import CORS

RADIUS = 200

app = Flask(__name__)
CORS(app)

model = None
parking_meters = None


@app.before_first_request
def startup():
    global model
    # global model, parking_meters
    # # pedir data de los parkingmeters (http://localhost:4567/parking_meters/all)
    # r = requests.get("http://localhost:4567/parking_meters/all")
    # parking_meters = r.json()

    my_file = Path("./models/model.pkl")
    if not my_file.is_file():
        dump_model()
    model = pickle.load(open("./models/model.pkl", "rb"))
    if model is not None:
        print("Model loaded!")
    else:
        print("Model not loaded!")


@app.route("/")
def first_page():
    return jsonify("Parking Recommender")


@app.route('/predict', methods=['POST'])
def predict():
    print(request.get_json())
    if (request.get_json() is None) or (request.get_json() == ""):
        return make_response("The request does not have the necessary parameters", 200)
    try:
        # feature_array = request.get_json()['feature_array']
        lat = request.get_json()['lat']
        lon = request.get_json()['lon']
        time = get_index(request.get_json()['time'])
        dow = request.get_json()['dow']
        r = requests.post("http://127.0.0.1:2525/nearest_parking", json={"lat": lat, "lon": lon})
        nearest_parkingmeters = r.json()
        ret = []
        for parkingmeter in nearest_parkingmeters['nearest_parking']:
            prediction = model.predict([[parkingmeter['id'], time, dow]])
            json_object = {'id': parkingmeter['id'], 'lat': parkingmeter['lat'], 'lon': parkingmeter['lon'],
                           'prediction': prediction[0]}
            ret.append(json_object)
        print("Request completed!")
        print(ret)
        return make_response(jsonify(ret), 200)
    except requests.RequestException:
        return make_response("Error at connection", 200)


@app.errorhandler(400)
def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
    }
    resp = jsonify(message)
    resp.status_code = 400
    return resp


if __name__ == '__main__':
    app.run()

