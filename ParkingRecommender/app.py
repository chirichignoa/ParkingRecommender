from datetime import datetime, timedelta

from flask import jsonify, request, make_response
from flask_cors import CORS
# from app import *

import requests
from flask import Flask

PARKING_METERS_SERVICE = {
    'HOST': "http://parkingmeters-service",
    'PORT': '2500',
    'PATH': "parking_meters/all"
}
HAVERSINE_DISTANCE_SERVICE = {
    'HOST': "http://coordinate-distance-service",
    'PORT': '3500',
    'PATH': "distance/get_distance"
}
PARKING_RECOMMENDER_SERVICE = {
    'HOST': "http://parking-recommender-service",
    'PORT': '4500',
    'PATH': "predict"
}

app = Flask(__name__)
# app.config.from_object(config[config_name])
# app.config.from_pyfile('config.py', silent=True)

CORS(app)

parking_meters = []
times = []
RADIUS = 200


def get_index(time):
    return times.index(time)


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def get_parkingmeters():
    global parking_meters
    try:
        r = requests.get(PARKING_METERS_SERVICE['HOST'] + ":" +
                         PARKING_METERS_SERVICE['PORT'] + "/" +
                         PARKING_METERS_SERVICE['PATH'])
        parking_meters = r.json()
        print(parking_meters)
    except requests.RequestException:
        print("Error at connection")


def get_nearest_parkingmeters(lat, lon):
    ret = []
    for parkingmeter in parking_meters:
        payload = {'lat_s': lat, 'lon_s': lon, 'lat_d': parkingmeter['lat'], 'lon_d': parkingmeter['lon']}
        r = requests.get(HAVERSINE_DISTANCE_SERVICE['HOST'] + ":" +
                         HAVERSINE_DISTANCE_SERVICE['PORT'] + "/" +
                         HAVERSINE_DISTANCE_SERVICE['PATH'],
                         params=payload)
        distance = r.json()
        if distance <= RADIUS:
            parkingmeter['distance'] = distance
            ret.append(parkingmeter)
    return ret


@app.before_first_request
def startup():
    global times
    times = [dt.strftime('%H:%M') for dt in
             datetime_range(datetime(2018, 1, 1, 10, 0), datetime(2018, 1, 1, 20, 15),
                            timedelta(minutes=15))]
    get_parkingmeters()


@app.route('/prediction', methods=['GET'])
def get_prediction():
    # if (request.get_json() is None) or (request.get_json() == ""):
    #     return make_response("The request does not have the necessary parameters", 400)
    ret = []
    lat = request.get_json()['lat']
    lon = request.get_json()['lon']
    time = get_index(request.get_json()['time'])
    dow = request.get_json()['dow']
    nearest_parkingmeters = get_nearest_parkingmeters(lat, lon)
    for parkingmeter in nearest_parkingmeters['nearest_parking']:
        payload = {'id_cuadra': parkingmeter['id'], 'time': time, 'dow': dow}
        prediction = requests.get(PARKING_RECOMMENDER_SERVICE['HOST'] + ":" +
                                  PARKING_RECOMMENDER_SERVICE['PORT'] + "/" +
                                  PARKING_RECOMMENDER_SERVICE['PATH'],
                                  params=payload).json()
        json_object = {'id': parkingmeter['id'], 'lat': parkingmeter['lat'], 'lon': parkingmeter['lon'],
                       'prediction': prediction[0], 'dir': parkingmeter['direccion']}
        ret.append(json_object)
    return make_response(jsonify(ret), 200)


if __name__ == '__main__':
    app.run()
