# -*- encoding:utf-8 -*-
import pandas as pd
from sklearn.model_selection import KFold
from ultron.optimize.model.modelbase import load_module


def model_fitness(features, model_name, X, Y, params, default_value, mode,
                  n_splits):
    kf = KFold(n_splits=n_splits, shuffle=False)
    res = []
    for train_index, test_index in kf.split(X):
        x_train = X.iloc[train_index]
        y_train = Y.iloc[train_index].values
        x_test = X.iloc[test_index]
        y_test = Y.iloc[test_index].values
        model = load_module(model_name)(features=features, **params)
        model.fit(x_train, y_train)
        res.append({mode: model.__getattribute__(mode)(x_test, y_test)})
    result = pd.DataFrame(res)
    return default_value if result.empty else result[mode].mean()