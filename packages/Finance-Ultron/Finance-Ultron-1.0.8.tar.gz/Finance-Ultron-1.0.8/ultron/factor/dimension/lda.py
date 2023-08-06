# -*- encoding:utf-8 -*-
"""
    LDA降维
"""
import numpy as np
import pandas as pd
from six.moves import xrange
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from ultron.utilities.logger import kd_logger
from ultron.kdutils.progress import Progress


class LDA(object):

    def __init__(self, features=None):
        self._features = features

    def evaluate_model(self, model, X, y):
        cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
        scores = cross_val_score(model,
                                 X,
                                 y,
                                 scoring='accuracy',
                                 cv=cv,
                                 n_jobs=-1,
                                 error_score='raise')
        return scores

    def fetch_models(self, best_k):
        models = {}
        for i in range(1, best_k):
            steps = [('lda', LinearDiscriminantAnalysis(n_components=i)),
                     ('m', GaussianNB())]
            models[str(i)] = Pipeline(steps=steps)
        return models

    def fit_lda(self, X, y, best_k):
        results = []
        i = 0
        models = self.fetch_models(best_k=best_k)
        with Progress(len(models), 0, 'fit LDA') as pg:
            for name, model in models.items():
                i += 1
                scores = self.evaluate_model(model, X, y)
                results.append({
                    'name': name,
                    'mean': np.mean(scores),
                    'std': np.std(scores)
                })
                pg.show(i)
        results = pd.DataFrame(results).sort_values(by='mean', ascending=False)
        return int(results['name'].values[0])

    def run(self, factors_data, best_k):
        n_components = self.fit_lda(X=factors_data[self._features].values,
                                    y=factors_data['cluster'].values,
                                    best_k=best_k)
        dimension_factor = LinearDiscriminantAnalysis(
            n_components=n_components).fit_transform(
                factors_data[self._features].values,
                factors_data['cluster'].values,
            )
        dimension_name = [
            "lda_{0}_{1}".format(n_components, k)
            for k in xrange(1, n_components + 1)
        ]
        dimension_factor = pd.DataFrame(dimension_factor,
                                        columns=dimension_name)
        return dimension_factor
