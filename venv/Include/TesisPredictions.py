#SENTENCIA PARA ACTIVAR VIRTUAL ENVIROMENT: cmd y luego venv\Scripts\activate
from flask import Flask, jsonify, abort
from flask import make_response
from flask import request
import predictionController
import time
import atexit
import pandas as pd
import numpy as np

app = Flask(__name__)

contPredictions = predictionController.predictionController()
@app.route('/stockPrediction/getNextFromHistory', methods=['POST'])
def get_Predictinos_History():
    reqData = request.get_json()
    ticker = reqData['ticker']
    key = reqData['api-key']
    listaHist = reqData['historico']
    print(type(listaHist))
    if (key=="MASTER"):
        tick,pred,change = contPredictions.dailyPrediction(ticker,np.array(listaHist))
        return jsonify(ticker=tick,prediction=pred,increase=change)
    else:
        return jsonify(message="Api-key incorrecta")

#Error Mapping
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",threaded=False,use_reloader=False)
