import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pickle
from pathlib import Path
import json
import pandas as pd


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
        user_data = self.fetch_from_redis(member_id)

        if len(user_data.index) < 1:
            print(f'{member_id} has no user interactions')
            return []
        
        # get predictions
        raw_predictions = self._model.predict(user_data)

        if len(raw_predictions.brand.keys()) < 1:
            print(f'{member_id} has no user interactions')
            return []
            
        raw_predictions = raw_predictions.__dict__

        predictions = list()
        for k in raw_predictions["brand"]:
            predictions.append({
                "brand_id": raw_predictions["brand"][k],
                "score": raw_predictions["score"][k],
                "liked": raw_predictions["liked"][k],
                "gender": raw_predictions["gender"][k],
                "category_ids": [int(x) for x in raw_predictions["category"][k].split(',')],
            })

        return predictions
    

    def fetch_from_redis(self, member_id):
        with open('user-data-redis.txt', 'r') as file:
            user_data = file.read().replace('\n', '')
        if user_data is not None:
            return pd.read_json(user_data)
        return []
