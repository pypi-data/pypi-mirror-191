# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class Universe(object):

    @classmethod
    def fix(cls, data):
        nrow, ncol = data.shape
        rval = np.full(shape=[nrow, ncol], fill_value=True)
        rval = pd.DataFrame(rval, index=data.index, columns=data.columns)

        products = [
            'A', 'AG', 'AL', 'AU', 'BU', 'C', 'CF', 'CS', 'CU', 'FG', 'HC',
            'I', 'J', 'JM', 'L', 'M', 'MA', 'NI', 'OI', 'P', 'PP', 'RB', 'RM',
            'RU', 'SR', 'TA', 'V', 'Y', 'ZC', 'ZN'
        ]

        for col in data.columns:
            if col not in products:
                rval[col] = False

        return rval

    @classmethod
    def single(cls, data, product):
        rval = pd.DataFrame(False, index=data.index, columns=data.columns)

        if isinstance(product, str):
            products = [product]
        else:
            products = product

        rval[products] = True

        return rval

    @classmethod
    def all(cls, data):
        assert isinstance(data, pd.DataFrame)
        rval = pd.DataFrame(True, index=data.index, columns=data.columns)
        return rval

    @classmethod
    def index_pair(cls, data):
        nrow, ncol = data.shape
        rval = np.full(shape=[nrow, ncol], fill_value=True)
        rval = pd.DataFrame(rval, index=data.index, columns=data.columns)
        products = ['IF', 'IM', 'IH', 'IC']
        for col in data.columns:
            if col not in products:
                rval[col] = False

        return rval