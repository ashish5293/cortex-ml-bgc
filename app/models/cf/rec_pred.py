import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from app.entities.model.model import Model
from app.entities.model.prediction import Prediction
from app.utils.exception_decorator import exception_decorator


class RecPred(Model):
    REC_PARAM = dict(n_rec=150)
    MODEL_FILE_NAME = 'bgc_model.pkl'
    name = 'CF'
    version = '1.0'

    def __init__(self, cf_sim_mat,
                 cf_item_dict):
        Model.__init__(self)
        self.cf_sim_mat = cf_sim_mat
        self.cf_item_dict = cf_item_dict
        self.n_rec = RecPred.REC_PARAM['n_rec']

    @staticmethod
    def _post_process_rec(dataset) -> pd.DataFrame:
        """
        Process recommendation list
        :param dataset
        :return dataset
        """

        dataset = dataset.copy()

        dataset.brand = dataset.brand.astype('int16')
        dataset.gender = dataset.gender.astype('int8')

        dataset = dataset.assign(log_score=lambda x: np.log1p(x.score))
        dataset.drop(columns=['score'], axis=1, inplace=True)
        dataset = dataset.assign(norm_score=lambda x: x.log_score / dataset.log_score.max())
        dataset.rename(columns={'norm_score': 'score'}, inplace=True)
        dataset.score = np.round(dataset.score, decimals=6)

        return dataset[['brand', 'gender', 'category', 'score', 'liked']]

    @exception_decorator
    def _rec_predict(self, user_data, sim_mat: csr_matrix, item_dict: dict) -> pd.DataFrame:

        """
        :return recommendations for each user in the dataset
        """

        user_data_dict = dict(zip(user_data.b_g_c, user_data.total_hits))

        user_items = np.array([user_data_dict.get(item_dict.get(k), 0) for k in item_dict.keys()])

        user_items = user_items.reshape(1, -1)
        user_items = csr_matrix(user_items)

        # Compute dot product
        rec_mat = user_items @ sim_mat

        result = []
        liked = set(user_items.indices)
        user_indices, user_scores = rec_mat.indices, rec_mat.data
        best = sorted(zip(user_indices, user_scores), key=lambda x: -x[1])
        tagged_best = [rec + (True,) if rec[0] in liked else rec + (False,) for rec in best][: self.n_rec]
        result.extend([(item_dict[rid].split(' ')[0], item_dict[rid].split(' ')[1], item_dict[rid].split(' ')[2],
                        score, flag_brx) for rid, score, flag_brx in tagged_best])

        rec = pd.DataFrame(result, columns=['brand', 'gender', 'category', 'score', 'liked'])

        if rec.score.lt(0).any():
            return pd.DataFrame(columns=['brand', 'gender', 'category', 'score', 'liked'])

        if len(rec.index) == 0:
            return pd.DataFrame(columns=['brand', 'gender', 'category', 'score', 'liked'])

        return RecPred._post_process_rec(rec)

    @exception_decorator
    def predict(self, data) -> Prediction:
        rec_dict = self._rec_predict(data, sim_mat=self.cf_sim_mat, item_dict=self.cf_item_dict).to_dict()
        return Prediction(rec_dict['brand'], rec_dict['gender'],
                          rec_dict['category'], rec_dict['score'], rec_dict['liked'])
