# -*- coding: utf-8 -*-
import os, pdb, itertools, copy, datetime, sys, json
import pandas as pd

os.environ['ULTRON_DATA'] = 'keim'
from ultron.env import *
from ultron.sentry.api import *
from ultron.optimize.model.treemodel import RandomForestRegressor
from ultron.optimize.model.treemodel import RandomForestClassifier

enable_example_env()

train_data = pd.read_csv(os.path.join(g_project_data, 'train_datas.csv'),
                         index_col=0)

featrues = [
    MSUM(10, 'BM_MainFar_80D'), 'BM_RecentFar_40D',
    'WeightShortVolRelTotIntChg'
]
train_data['trade_date'] = pd.to_datetime(train_data['trade_date'])
model = RandomForestClassifier(features=featrues)
#model.formulas.transform('code', cmt)
#pdb.set_trace()
#model.fit(train_data[featrues].fillna(0),
#          train_data['signal'].fillna(0).values)
#print('--->')