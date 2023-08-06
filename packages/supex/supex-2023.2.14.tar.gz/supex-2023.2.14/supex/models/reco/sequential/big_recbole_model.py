import os
from pathlib import Path
import pandas as pd
from pytz import timezone
import logging
from logging import getLogger

from recbole.config import Config
from recbole.data import create_dataset, data_preparation
import recbole.model.sequential_recommender as sequential_model
from recbole.utils.case_study import full_sort_topk
from recbole.trainer import Trainer
from recbole.utils import init_seed, init_logger

TZ = timezone("Asia/Seoul")


class DeepSeqEurekaModel:
    """
    recbole을 활용한 여러 sequential model 활용 클래스
    """

    def __init__(
        self,
        model_name: str,
        model_version: str,
        data: pd.DataFrame,
        data_type,
        user_id: str,
        item_id: str,
        timestamp: str,
        parameter_dict: dict = {},
        data_dir: str = None,
    ) -> None:

        assert isinstance(model_name, str), "`model_name`은 str 타입이어야 합니다."
        assert isinstance(model_version, str), "`model_version`은 str 타입이어야 합니다."
        assert isinstance(user_id, str), "`user_id`은 str 타입이어야 합니다."
        assert isinstance(item_id, str), "`item_id`은 str 타입이어야 합니다."
        assert isinstance(timestamp, str), "`timestamp`은 str 타입이어야 합니다."
        assert isinstance(parameter_dict, dict), "`parameter_dict`은 dict 타입이어야 합니다."

        if data_dir:
            assert isinstance(data_dir, str), "`data_dir`은 str 타입이어야 합니다."
        else:
            data_dir = f"{str(Path.home())}/myfiles/supex_data"

        name = f"{model_name}_{model_version}"

        if os.path.exists(f"{data_dir}/{name}/"):
            pass
        else:
            os.makedirs(f"{data_dir}/{name}/")

        self.data_dir = data_dir
        self.user_id = user_id
        self.item_id = item_id
        self.timestamp = timestamp
        self.model_name = model_name
        self.name = name

        if parameter_dict:
            pass
        else:
            parameter_dict = {
                "user_inter_num_interval": "[5,Inf)",
                "item_inter_num_interval": "[5,Inf)",
                "train_neg_sample_args": {
                    "distribution": "uniform",
                    "sample_num": 1,
                    "alpha": 1.0,
                    "dynamic": False,
                    "candidate_num": 0,
                },
                "MAX_ITEM_LIST_LENGTH": 20,
                "eval_args": {
                    "split": {"RS": [0.8, 0.1, 0.1]},
                    "order": "RO",
                    "group_by": "user",
                    "mode": "full",
                },
            }

        parameter_dict.update(
            {
                "data_path": f"{self.data_dir}",
                "USER_ID_FIELD": f"{self.user_id}",
                "ITEM_ID_FIELD": f"{self.item_id}",
                "TIME_FIELD": f"{self.timestamp}",
                "load_col": {"inter": [self.user_id, self.item_id, self.timestamp]},
            }
        )
        self.parameter_dict = parameter_dict

        if data_type:
            re_col = {}
            for i in data_type:
                for j in data_type[i]:
                    re_col[j] = f"{j}:{i}"

            for key, value in data.items():
                data[key] = value.rename(columns=re_col)
                cols = [i for i in data[key].columns if i in list(re_col.values())]
                data[key][cols].to_csv(f"{data_dir}/{name}/{name}.{key}", index=False, sep="\t")
        else:
            for key, value in data.items():
                data[key] = value.rename(
                    columns={user_id: "user_id:token", item_id: "item_id:token", timestamp: "timestamp:float"}
                )
                data[key][["user_id:token", "item_id:token", "timestamp:float"]].to_csv(
                    f"{data_dir}/{name}/{name}.{key}", index=False, sep="\t"
                )

        self.data = data
        self.re_col = re_col

    def _preprocessing(self):
        config = Config(model=self.model_name, dataset=self.name, config_dict=self.parameter_dict)

        # init random seed
        init_seed(config["seed"], config["reproducibility"])

        # logger initialization
        init_logger(config)
        logger = getLogger()

        # Create handlers
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        logger.addHandler(c_handler)

        # write config info into log

        self.dataset = create_dataset(config)

        # dataset splitting
        train_data, valid_data, test_data = data_preparation(config, self.dataset)

        self.config = config
        return train_data, valid_data, test_data

    def _fit(
        self,
        train_data,
    ):
        # model loading and initialization
        seq_reco = getattr(sequential_model, self.model_name)
        self.model = seq_reco(self.config, train_data.dataset).to(self.config["device"])

        # trainer loading and initialization
        self.trainer = Trainer(self.config, self.model)

        # model training
        best_valid_score, best_valid_result = self.trainer.fit(train_data)
        return best_valid_score

    def _predict(
        self,
        test_data,
        nums=10,
        topk=10,
    ):
        if nums is None:
            nums = self.dataset.user_num

        external_user_ids = self.dataset.id2token(self.dataset.uid_field, list(range(nums)))[1:]
        topk_items = []
        for internal_user_id in list(range(nums))[1:]:
            _, topk_iid_list = full_sort_topk(
                [internal_user_id], self.model, test_data, k=topk, device=self.config["device"]
            )
            last_topk_iid_list = topk_iid_list[-1]
            external_item_list = self.dataset.id2token(self.dataset.iid_field, last_topk_iid_list.cpu()).tolist()
            topk_items.append(external_item_list)

        external_item_str = [" ".join(x) for x in topk_items]
        result = pd.DataFrame(external_user_ids, columns=["user_id"])
        result["prediction"] = external_item_str
        return result

    def fit_predict(
        self,
        nums=10,
        topk=10,
    ):
        train_data, valid_data, test_data = self._preprocessing()
        self._fit(train_data)
        return self._predict(test_data, nums, topk)

    def get_evaluation(
        self,
    ):
        train_data, valid_data, test_data = self._preprocessing()
        self._fit(train_data)
        return self.trainer.evaluate(test_data)
