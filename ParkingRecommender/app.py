from datetime import datetime, timedelta

from flask import jsonify, request, make_response
from flask_cors import CORS
# from app import *

import requests
from flask import Flask

PARKING_METERS_SERVICE = {
    'HOST': "http://parkingmeters-service",
    'PORT': '4567',
    'PATH': "parking_meters/all"
}
HAVERSINE_DISTANCE_SERVICE = {
    'HOST': "http://haversine-distance-service",
    'PORT': '2525',
    'PATH': "calculate_distance"
}
PARKING_RECOMMENDER_SERVICE = {
    'HOST': "http://recommender-service",
    'PORT': '5000',
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
    except requests.RequestException:
        print("Error at connection")


@app.route('/nearest', methods=['GET'])
def nearest_parkingmeters():
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    asd = get_nearest_parkingmeters(lat, lon)
    return make_response(jsonify(asd), 200)


def get_nearest_parkingmeters(lat, lon):
    ret = []
    for parkingmeter in parking_meters:
        payload = {'lat_s': lat, 'lng_s': lon, 'lat_d': parkingmeter['lat'], 'lng_d': parkingmeter['lon']}
        r = requests.get(HAVERSINE_DISTANCE_SERVICE['HOST'] + ":" +
                         HAVERSINE_DISTANCE_SERVICE['PORT'] + "/" +
                         HAVERSINE_DISTANCE_SERVICE['PATH'],
                         params=payload)
        distance = r.json()['distance']
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
    ret = []
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    time = request.args.get('time', None)
    dow = request.args.get('dow', None)
    if (lat is None) or (lon is None) or (time is None) or (dow is None):
        return make_response("The request does not have the necessary parameters", 400)
    time = get_index(time)
    nearest_parkingmeters = get_nearest_parkingmeters(lat, lon)
    for parkingmeter in nearest_parkingmeters:
        payload = {'id_cuadra': parkingmeter['id'], 'time': time, 'dow': dow}
        prediction = requests.get(PARKING_RECOMMENDER_SERVICE['HOST'] + ":" +
                                  PARKING_RECOMMENDER_SERVICE['PORT'] + "/" +
                                  PARKING_RECOMMENDER_SERVICE['PATH'],
                                  params=payload).json()
        json_object = {'id': parkingmeter['id'], 'lat': parkingmeter['lat'], 'lon': parkingmeter['lon'],
                       'prediction': prediction['prediction'], 'dir': parkingmeter['direccion']}
        ret.append(json_object)
    return make_response(jsonify(ret), 200)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run()
