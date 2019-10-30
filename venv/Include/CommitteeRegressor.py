import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True
class CommitteeRegressor():
  def __init__(self):
    self.committeeSize=0
    self.listaMiembros=[]
    self.voting="Simple"
    self.dictPesos={}
  def addMember(self,regressor):
    self.listaMiembros.append((regressor.ticker,regressor))
    self.committeeSize=self.committeeSize+1
  def predict(self,ticker,history):
    if (self.voting=="Simple"):
      i=0
      sumaTotal=0
      for tickerMember,member in self.listaMiembros:
        if (tickerMember==ticker):
          prediction = member.predict(history)
          sumaTotal=sumaTotal+prediction
          i=i+1
      return (sumaTotal/i)
    if (self.voting=="Stacking"):
      sumaTotal=0
      i=0
      for tickerMember,member in self.listaMiembros:
        if (tickerMember==ticker):
          prediction = member.predict(history)
          sumaTotal=sumaTotal+prediction*(self.dictPesos[ticker][i])
          i=i+1
      return (sumaTotal+self.dictPesos[ticker][i])