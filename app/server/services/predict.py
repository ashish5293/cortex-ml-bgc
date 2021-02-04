from typing import List
from ssense_logger.app_logger import AppLogger

from app.entities.model.model import Model
from app.server.entities.prediction import Prediction
from app.repositories.redis_repository import RedisRepository


class PredictService:
    _model = None

    def __init__(self,
                 model: Model,
                 app_logger: AppLogger,
                 customer_bgc_scores_repository: RedisRepository):
        self._model = model
        self.app_logger = app_logger
        self.customer_bgc_scores_repository = customer_bgc_scores_repository

    def predict(self, member_id: int, request_id: str) -> List[Prediction]:
        # Load user data directly from redis
        user_data = self.customer_bgc_scores_repository.get_by_member_id(member_id)
        if len(user_data.index) < 1:
            self.app_logger.info(msg=f'{member_id} has no user interactions',
                                 tags=['PredictService', 'no_user_interactions'],
                                 request_id=request_id)
            return []

        raw_predictions = self._model.predict(user_data)

        if len(raw_predictions.brand.keys()) < 1:
            self.app_logger.info(msg=f'{member_id} has no user interactions',
                                 tags=['PredictService', 'mo prediction'],
                                 request_id=request_id)
            return []

        predictions = list(map(
            lambda k: Prediction(
                brand_id=raw_predictions.brand[k],
                category_ids=[int(x) for x in raw_predictions.category[k].split(',')],
                gender=raw_predictions.gender[k],
                score=raw_predictions.score[k],
                liked=raw_predictions.liked[k]
            ), raw_predictions.brand.keys()))

        return predictions
