import pickle

from flask import Flask, jsonify, request, make_response
from pathlib import Path
from util.predictor import dump_model, get_index
import requests

RADIUS = 200

app = Flask(__name__)

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
    if (request.get_json() is None) or (request.get_json() == ""):
        resp = make_response("The request does not have the necessary parameters", 200)
        return resp
    try:
        # feature_array = request.get_json()['feature_array']
        lat = request.get_json()['lat']
        lon = request.get_json()['lon']
        print("Predictor: Getting for " + str(lat) + " " + str(lon))
        time = get_index(request.get_json()['time'])
        dow = request.get_json()['dow']
        r = requests.post("http://127.0.0.1:2525/nearest_parking", {'lat': lat, 'lon': lon})
        # nearest_parkingmeters = r.json()
        print(r)
        prediction = "asd"
        # calcular predicciones
        # generar json con id_cuadra, lat, lon, prediccion

        # prediction = model.predict([lat, lon, time, dow]).tolist()
        return make_response(jsonify({'prediction': prediction}), 200)
    except requests.RequestException:
        resp = make_response("Error at connection", 200)
        return resp


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

