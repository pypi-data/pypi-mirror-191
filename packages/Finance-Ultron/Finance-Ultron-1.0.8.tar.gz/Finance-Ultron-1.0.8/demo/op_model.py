# -*- coding: utf-8 -*-
import os, pdb, itertools, copy, datetime, sys, json

os.environ['ULTRON_DATA'] = 'keim'

import numpy as np
import pandas as pd
from ultron.env import *
from ultron.utilities.utils import NumpyEncoder
from ultron.optimize.geneticist.engine import Engine
from ultron.optimize.model.treemodel import XGBRegressor
from ultron.optimize.model.treemodel import LGBMRegressor
from ultron.optimize.model.treemodel import RandomForestRegressor

enable_example_env()

train_data = pd.read_csv(os.path.join(g_project_data, 'train_datas.csv'),
                         index_col=0)


class Parameter(object):

    @classmethod
    def RandomForestRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(80, 180, 10)],
            'max_depth': [i for i in range(3, 5, 2)],
            'max_features': ['auto', 'sqrt', 'log2']
        }

    @classmethod
    def ExtraTreesRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(80, 180, 10)],
            'max_depth': [i for i in range(3, 5, 2)],
            'max_features': ['auto', 'sqrt', 'log2']
        }

    @classmethod
    def BaggingRegressor(cls, **kwargs):
        return {
            'n_estimators': [i for i in range(80, 180, 10)],
            'max_depth': [i for i in range(3, 5, 2)],
            'max_features': ['auto', 'sqrt', 'log2']
        }

    @classmethod
    def XGBRegressor(cls, **kwargs):
        return {
            'max_depth': [i for i in range(6, 15, 2)],
            'n_estimators': [i for i in range(50, 150, 10)],
            'learning_rate': [(i / 100) for i in range(1, 10, 2)]
        }

    @classmethod
    def LGBMRegressor(cls, **kwargs):
        return {
            'max_depth': [i for i in range(6, 15, 2)],
            'n_estimators': [i for i in range(50, 150, 10)],
            'learning_rate': [(i / 100) for i in range(1, 10, 2)]
        }


params_sets = {
    'XGBRegressor': Parameter.XGBRegressor(),
    'RandomForestRegressor': Parameter.RandomForestRegressor(),
    'LGBMRegressor': Parameter.LGBMRegressor(),
}

model_sets = ['XGBRegressor', 'RandomForestRegressor', 'LGBMRegressor']

features = [
    col for col in train_data.columns if col not in
    ['trade_date', 'code', 'value', 'signal', 'inventory', 'profitratio']
]

X = train_data[['trade_date', 'code'] + features].set_index(
    ['trade_date', 'code']).fillna(0)
Y = train_data[['trade_date', 'code',
                'signal']].set_index(['trade_date', 'code']).fillna(0)
Y = pd.DataFrame(np.random.randn(len(X)), index=Y.index, columns=['signal'])


def save_model(gen, rootid, sessionid, run_details):  ## 每一代优秀模型回调
    res = []
    pdb.set_trace()
    for detail in run_details:
        features = detail._identification
        model_name = detail._model_name
        params = json.dumps(detail._params, cls=NumpyEncoder)
        fitness = detail._raw_fitness
        method = detail._init_method
        res.append({
            'features': features,
            'model_name': model_name,
            'params': params,
            'fitness': fitness,
            'gen': gen,
            'method': method
        })


custom_params = {
    'begin_date': '2020-01-01',
    'end_date': '2022-01-01',
    'yields': 'ret',
    'rootid': '10001',
    'thresh': 0.98
}

gentic = Engine(model_sets=model_sets,
                params_sets=params_sets,
                convergence=0.002,
                population_size=20,
                tournament_size=5,
                p_point_mutation=0.7,
                p_crossover=0.2,
                standard_score=0.2,
                stopping_criteria=-100,
                custom_params=custom_params,
                rootid='100001',
                greater_is_better=False,
                save_model=save_model)

gentic.train(features, X=X, Y=Y, mode='mse', n_splits=2)  # mode 为模型评估方式
