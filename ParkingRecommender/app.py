from datetime import datetime, timedelta

from flask import Flask, request, make_response

app = Flask(__name__)
times = []


# times = ["10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45", "12:00", "12:15", "12:30", "12:45",
#          "13:00", "13:15", "13:30", "13:45", "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45",
#          "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30",  "18:45",
#          "19:00", "19:15", "19:30", "19:45", "20:00"]


def get_index(time):
    return times.index(time)


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


@app.before_first_request
def startup():
    global times
    times = [dt.strftime('%H:%M') for dt in
             datetime_range(datetime(2018, 1, 1, 10, 0), datetime(2018, 1, 1, 20, 15),
                            timedelta(minutes=15))]
    print(times);


@app.route('/prediction', methods=['GET'])
def get_prediction():
    if (request.get_json() is None) or (request.get_json() == ""):
        return make_response("The request does not have the necessary parameters", 200)
    # try:
    # feature_array = request.get_json()['feature_array']
    lat = request.get_json()['lat']
    lon = request.get_json()['lon']
    time = get_index(request.get_json()['time'])
    dow = request.get_json()['dow']
    return make_response("its okay")
    # except requests.RequestException:
    #     return make_response("Error at connection", 200)


if __name__ == '__main__':
    app.run()
