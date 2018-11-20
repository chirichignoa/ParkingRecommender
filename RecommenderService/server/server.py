import pickle
from flask import jsonify, request, make_response
from pathlib import Path
from util.predictor import dump_model
from flask_cors import CORS
from server import app

CORS(app)

model = None


@app.before_first_request
def startup():
    global model
    my_file = Path("./models/model.pkl")
    if not my_file.is_file():
        dump_model()
    model = pickle.load(open("./models/model.pkl", "rb"))
    if model is not None:
        print("Model loaded!")
    else:
        print("Model not loaded!")


@app.route('/predict', methods=['GET'])
def predict():
    id_cuadra = request.args.get('id_cuadra', None)
    time = request.args.get('time', None)
    dow = request.args.get('dow', None)
    if (id_cuadra is None) or (time is None) or (dow is None):
        return make_response("The request does not have the necessary parameters", 400)
    prediction = model.predict([[int(id_cuadra), int(time), int(dow)]])
    json_object = {'prediction': prediction[0]}
    return make_response(jsonify(json_object), 200)


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

