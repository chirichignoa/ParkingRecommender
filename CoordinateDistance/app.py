from flask import Flask, jsonify, request, make_response
from pathlib import Path
import numpy as np
from math import *
import requests
from flask_cors import CORS

RADIUS = 200

parking_meters = None
app = Flask(__name__)
CORS(app)

@app.before_first_request
def startup():
    global parking_meters
    try:
        r = requests.get("http://localhost:4567/parking_meters/all")
        parking_meters = r.json()
    except requests.RequestException:
        print("Error at connection")


@app.route('/nearest_parking', methods=['POST'])
def get_nearest_parking_meters():
    print(request)
    lat = request.get_json()['lat']
    lon = request.get_json()['lon']
    print("Nearest-parking: " + str(lat) + " - " + str(lon))
    if parking_meters is None:
        return make_response(jsonify({'error': "No se puede conectar con otros servicios necesarios", 'code': 200}))
    return make_response(jsonify({'nearest_parking': calculate_distance(lat, lon)}), 200)


def calculate_distance(lat, lon):
    ret = []
    for parkingmeter in parking_meters:
        distance = float(get_haversine(lat, lon, parkingmeter['lat'], parkingmeter['lon']))
        if distance <= RADIUS:
            parkingmeter['distance'] = distance
            ret.append(parkingmeter)
    return ret


@app.route('/calculate_distance', methods=['POST'])
def get_distance():
    lat_s = request.get_json()['lat_s']
    lng_s = request.get_json()['lng_s']
    lat_d = request.get_json()['lat_d']
    lng_d = request.get_json()['lng_d']
    print("Getting haversine distance between: {} - {} - {} - {}".format(lat_s, lng_s, lat_d, lng_d))
    return make_response(jsonify({'distance': get_haversine(lat_s, lng_s, lat_d, lng_d)}), 200)


def get_haversine(lat_s, lng_s, lat_d, lng_d):
    earth_radius_km = 6371
    d_lat = degrees_to_radians(lat_d - lat_s)
    d_lon = degrees_to_radians(lng_d - lng_s)

    a = sin(d_lat / 2) * sin(d_lat / 2) + sin(d_lon / 2) * sin(d_lon / 2) * cos(lat_s) * cos(lat_d)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return (earth_radius_km * c) * 1000


def degrees_to_radians(degrees):
    return degrees * pi / 180


if __name__ == '__main__':
    app.run()
