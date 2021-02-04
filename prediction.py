from typing import List, Dict
from abc import ABC, abstractmethod
from datetime import datetime

class Prediction(dict):
    brand_id: int
    score: float
    liked: bool
    gender: int
    category_ids: List[int]

    def __init__(self, brand_id: int, category_ids: List[int], score: float, liked: bool, gender: int):
        self.brand_id = brand_id
        self.score = score
        self.liked = liked
        self.gender = gender
        self.category_ids = category_ids


class Model(ABC):
    version: str = None
    USE_CASE = 'BRAND_GENDER_CATEGORY'

    def __init__(self):
        self.init_date = datetime.now()

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def predict(self, data):
        class Prediction:
            def __init__(self, brand: Dict[int, int], gender: Dict[int, int], category: Dict[int, str], score: Dict[int, float], liked: Dict[int, bool]):
                self.brand = brand
                self.gender = gender
                self.category = category
                self.score = score
                self.liked = liked
        prediction = Prediction(
            {1: 1444, 2: 1333},
            {1: '55', 2: '43,46'},
            {1: 1, 2: 1},
            {1: 0.99, 2: 0.88},
            {1: True, 2: False}
        )
        return prediction
    
    '''
    def to_model_info(self) -> ModelInfo:
        return ModelInfo(
            usecase=self.USE_CASE,
            model=self.name,
            version=self.version,
            timestamp=self.init_date.strftime('%Y-%m-%d-%H-%M-%S')
        )
    '''
