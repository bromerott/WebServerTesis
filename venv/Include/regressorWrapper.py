import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import keras
import xgboost
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True
class RegressorWrapper():
  def __init__(self,tipo,ticker,regressor):
    self.tipo = tipo
    self.ticker=ticker
    self.regressor = regressor
  def predict(self, history):
    if self.tipo=='LSTM':
      #scale in respect to history
      sc = MinMaxScaler(feature_range = (0, 1))
      sc.fit(history.reshape(-1,1))
      inputs = history[len(history) - 60:len(history)]
      inputs = inputs.reshape(-1,1)
      inputs = sc.transform(inputs)
      #slice last 60
      X_test=[]
      X_test.append(inputs[:, 0])
      X_test = np.array(X_test)
      X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
      return sc.inverse_transform(self.regressor.predict(X_test))[0][0]
    if self.tipo=='PXGB':
      dayToDay = history[1:len(history)]-history[0:len(history)-1]
      scaler = StandardScaler()
      scaler.fit(dayToDay.reshape(-1,1))
      dayToDay = scaler.transform(dayToDay.reshape(-1,1))
      X_test=[]
      #XGB works with daily increase/decrease, so need to make X_test that instead
      X_test.append(scaler.transform(dayToDay[dayToDay.size-30:dayToDay.size].reshape(-1,1)))
      X_test = np.array(X_test)
      pred = self.regressor.predict(X_test[:,:,0])
      pred = scaler.inverse_transform(pred)
      lastValue = history[history.size-1]
      return (pred[0]+lastValue)
      #return scaler.inverse_ransform(self.regressor.predict(X_test).reshape(-1,1))[0][0]
    if self.tipo=='FFNN':
      #scale in respect to history
      sc = MinMaxScaler(feature_range = (0, 1))
      sc.fit(history.reshape(-1,1))
      inputs = sc.transform(history.reshape(-1,1))
      #slice last four
      X_test=[]
      X_test.append(inputs[history.shape[0]-4:history.shape[0], 0])
      X_test = np.array(X_test)
      X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
      return sc.inverse_transform(self.regressor.predict(X_test[:,:,0]))[0][0]