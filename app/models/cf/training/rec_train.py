from pandas import DataFrame
from pathlib import Path

from app.models.cf.rec_pred import RecPred
from app.models.cf.training.cf_train import CollabTrain
from app.utils.serialization import load_pickle
from app.entities.model.model import Model
from app.entities.trainer.trainer import Trainer


class RecTrain(Trainer):

    def train(self, hits_data: DataFrame = None,) -> Model:
        if hits_data is None:
            hits_data = RecTrain._load_data_local()

        cf_sim_mat, cf_item_dict = CollabTrain(hits_data).fit()

        rec_pred = RecPred(cf_sim_mat=cf_sim_mat,
                           cf_item_dict=cf_item_dict)

        return rec_pred

    @staticmethod
    def _load_data_local() -> object:
        return load_pickle(directory=Path('./shared/'), name='hits_df.pkl')
