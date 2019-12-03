import pandas as pd
import numpy as np
import pickle
from regressorWrapper import RegressorWrapper
from CommitteeRegressor import CommitteeRegressor
class predictionController:

    dfPredictions = pd.DataFrame()
    def __init__(self):
        #Carga de dictSeries
        #Carga de diccionario de datos
        filehandler = open('dictSeries.obj', 'rb')
        dictSeries = pickle.load(filehandler)
        dictSeries
        print("Series cargadas")
        #Carga de modelos XGBoost
        #Carga de XGB
        dictXGB={}
        for entrada in dictSeries:
            tagModelo = "PXGB-"+entrada
            filehandler = open(tagModelo+".obj", 'rb')
            dictXGB[tagModelo]=pickle.load(filehandler)
        print("Modelos XGB Cargados")
        #Carga de LSTM
        dictLSTM={}
        for entrada in dictSeries:
            tagModelo = "LSTM-"+entrada
            filehandler = open(tagModelo+".obj", 'rb')
            dictLSTM[tagModelo]=pickle.load(filehandler)
        print("Modelos LSTM Cargados")

        #Carga de FFNN
        dictFFNN={}
        for entrada in dictSeries:
            tagModelo = "FFNN-"+entrada
            filehandler = open(tagModelo+".obj", 'rb')
            dictFFNN[tagModelo]=pickle.load(filehandler)
        print("Modelos FFNN Cargados")
        #Carga de Pesos
        filehandler = open('dictPesos.obj', 'rb')
        dictPesos = pickle.load(filehandler)
        print("Pesos Cargados")

        print("Inicializando Comite")
        self.comite = CommitteeRegressor()
        self.comite.voting="Stacking"
        self.comite.dictPesos=dictPesos

        self.comite.addMember(RegressorWrapper('PXGB','AMZN',dictXGB['PXGB'+'-'+'AMZN']))
        self.comite.addMember(RegressorWrapper('PXGB','DB',dictXGB['PXGB'+'-'+'DB']))
        self.comite.addMember(RegressorWrapper('PXGB','GOOGL',dictXGB['PXGB'+'-'+'GOOGL']))
        self.comite.addMember(RegressorWrapper('PXGB','WMT',dictXGB['PXGB'+'-'+'WMT']))
        self.comite.addMember(RegressorWrapper('PXGB','IBM',dictXGB['PXGB'+'-'+'IBM']))

        self.comite.addMember(RegressorWrapper('FFNN','AMZN',dictFFNN['FFNN'+'-'+'AMZN']))
        self.comite.addMember(RegressorWrapper('FFNN','DB',dictFFNN['FFNN'+'-'+'DB']))
        self.comite.addMember(RegressorWrapper('FFNN','GOOGL',dictFFNN['FFNN'+'-'+'GOOGL']))
        self.comite.addMember(RegressorWrapper('FFNN','WMT',dictFFNN['FFNN'+'-'+'WMT']))
        self.comite.addMember(RegressorWrapper('FFNN','IBM',dictFFNN['FFNN'+'-'+'IBM']))

        self.comite.addMember(RegressorWrapper('LSTM','AMZN',dictLSTM['LSTM'+'-'+'AMZN']))
        self.comite.addMember(RegressorWrapper('LSTM','DB',dictLSTM['LSTM'+'-'+'DB']))
        self.comite.addMember(RegressorWrapper('LSTM','GOOGL',dictLSTM['LSTM'+'-'+'GOOGL']))
        self.comite.addMember(RegressorWrapper('LSTM','WMT',dictLSTM['LSTM'+'-'+'WMT']))
        self.comite.addMember(RegressorWrapper('LSTM','IBM',dictLSTM['LSTM'+'-'+'IBM']))
    def dailyPrediction(self,ticker,history):
        lastValue = history[history.size-1]
        prediction = self.comite.predict(ticker,history)
        return (ticker,prediction,prediction-lastValue)