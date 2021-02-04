import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pickle
from prediction import Prediction
from pathlib import Path
import json
import pandas as pd

labels = ["setosa", "versicolor", "virginica"]


class PythonPredictor:
    

    def __init__(
        self, config
    ):
        # self._model = self.load_model_local(Path('model/model.pkl')) # load model here
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'model.pkl')
        self._model = pickle.load(open(filename, "rb"))
   
    def predict(self, payload):
        
        member_id = payload["member_id"]
        # Load user data directly from redis
        with open('user-data-redis.txt', 'r') as file:
            user_data = file.read().replace('\n', '')
        if user_data is not None:
            user_data = pd.read_json(user_data)
        

        if len(user_data.index) < 1:
            print(f'{member_id} has no user interactions')
            return []

        raw_predictions = self._model.predict(user_data)

        if len(raw_predictions.brand.keys()) < 1:
            print(f'{member_id} has no user interactions')
            return []
        raw_predictions = raw_predictions.__dict__
        print(raw_predictions)
        print(raw_predictions["brand"].keys())
        
        predictions = list()
        for k in raw_predictions["brand"]:
            predictions.append({
                "brand_id": raw_predictions["brand"][k],
                "score": raw_predictions["score"][k],
                "liked": raw_predictions["liked"][k],
                "gender": raw_predictions["gender"][k],
                "category_ids": [int(x) for x in raw_predictions["category"][k].split(',')],
            })
        '''
        predictions = list(map(
            lambda k: Prediction(
                brand_id=raw_predictions["brand"][k],
                category_ids=[int(x) for x in raw_predictions["category"][k].split(',')],
                gender=raw_predictions["gender"][k],
                score=raw_predictions["score"][k],
                liked=raw_predictions["liked"][k]
            ), raw_predictions["brand"].keys()))
        '''
        print(predictions)
        print(type(predictions))
        return predictions
    
        
    '''
    def __init__(self, config):
        if os.environ.get("AWS_ACCESS_KEY_ID"):
            s3 = boto3.client("s3")  # client will use your credentials if available
        else:
            s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))  # anonymous client

        s3.download_file(config["bucket"], config["key"], "/tmp/model.pkl")
        self.model = pickle.load(open("/tmp/model.pkl", "rb"))

    def predict(self, payload):
        measurements = [
            payload["sepal_length"],
            payload["sepal_width"],
            payload["petal_length"],
            payload["petal_width"],
        ]

        label_id = self.model.predict([measurements])[0]
        return labels[label_id]
    '''
