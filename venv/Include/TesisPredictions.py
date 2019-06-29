#SENTENCIA PARA ACTIVAR VIRTUAL ENVIROMENT: cmd y luego venv\Scripts\activate
from flask import Flask, jsonify, abort
from flask import make_response
from flask import request
import predictionController
import time
import atexit
import pandas as pd
import authenticationController

app = Flask(__name__)

contPredictions = predictionController.predictionController()
contAuthentication = authenticationController.authenticationController()
#GET Request to return today's predictions
@app.route('/TesisPredictions/getPredictions', methods=['GET'])
def get_Asignaciones():
    contPredictions.dailyPrediction()
    return jsonify({'Predictions':contPredictions.getPredictions()})

#POST Request to return today's predictions
@app.route('/TesisPredictions/authenticate', methods=['POST'])
def authenticate():
    reqData = request.get_json()
    email = reqData['email']
    password = reqData['password']
    return jsonify(contAuthentication.authenticate(email,password))

#POST Request to register new User
@app.route('/TesisPredictions/registerUser', methods=['POST'])
def register():
    reqData = request.get_json()
    email = reqData['email']
    password = reqData['password']
    contAuthentication.registerUser(email,password)
    return jsonify({'User': 'Registered'})

#Error Mapping
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
