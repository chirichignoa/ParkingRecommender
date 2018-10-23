# Coordinate Distance
Python microservice to calculate distance by given a latitude and longitude.

## Usage

Ensure that ParkingMetersService is running in 4567 port.
After:
```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run --port=2525
```

Now, you will be able to do HTTP request to the following pats:

| path 	| method 	| params 	| description 	|  	|
|---------------------	|--------	|-----------------------------------------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------	|---	|
| /nearest_parking 	| POST 	| lat: numeric value. lon: numeric value. 	| For given lat and lon, returns the nearest parking meters in a 200m radius. 	|  	|
| /calculate_distance 	| POST 	| lat_s: numeric value. lng_s: numeric value. lat_d: numeric value. lng_d: numeric value. 	| Calculate the haversine distance between (lat_s, lng_s) and (lat_d,lng_d). The result is expressed in KM. 	|  	|
|  	|  	|  	|  	|  	|
