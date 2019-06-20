#SENTENCIA PARA ACTIVAR VIRTUAL ENVIROMENT: cmd y luego venv\Scripts\activate
from flask import Flask, jsonify, abort
from flask import make_response
from flask import request
import predictions
import time
import atexit
import pandas as pd

app = Flask(__name__)

contPredictions = predictions.predictionController()

#Metodo de retorno de las Asignaciones
@app.route('/TesisPredictions/getPredictions', methods=['GET'])
def get_Asignaciones():
    contPredictions.dailyPrediction()
    return jsonify({'Predictions':contPredictions.getPredictions()})
    
#Metodo de mapeo de errores
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#Creacion de tarea daemon que ejecute el algoritmo de asignacion de vuelos cada 15 segundos
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
