import pandas as pd
class predictionController:

    dfPredictions = pd.DataFrame()

    def __init__(self):
        print("Pred Controller initialized")
        self.dfPredictions = pd.DataFrame(columns={'Id','CompanyName','CurrentPrice','PredictedPrice','Suggestion'})

    def dailyPrediction(self):
        self.dfPredictions = self.dfPredictions.append({'Id' : 1 , 'CompanyName' : 'Facebook','CurrentPrice':19.5,'PredictedPrice':19.2,'Suggestion':'SELL'} , ignore_index=True)

    def getPredictions(self):
        print ("Call to getPredictions")
        print (self.dfPredictions)
        return (self.dfPredictions.to_json(orient='records'))