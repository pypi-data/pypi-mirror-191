import os, copy, sys

os.environ['ULTRON_DATA'] = 'keim'
os.environ['IGNORE_WARNINGS'] = '0'
sys.path.insert(0, os.path.abspath('../'))
import pandas as pd
import numpy as np

from ultron.ump.technical.line import Line

from ultron.env import *

enable_example_env()

market_data = pd.read_csv('sz300059_20110728_20170726.csv', index_col=0)
market_data.head()

kl_tl = Line(market_data['close'][-252:], 'close')
rval = kl_tl.create_support_trend(only_last=True)