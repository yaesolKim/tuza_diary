# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.test import TestCase

# Create your tests here.
from pandas_datareader import data
import pandas as pd
import FinanceDataReader as fdr
import pyupbit

# 국내주식
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
# 해외주식
df_nasdaq = fdr.StockListing('NASDAQ')
# 코인


tickers = pyupbit.get_tickers()
print(tickers)
# 원화 시장의 코인 리스트
t = pyupbit.get_tickers(fiat="KRW")
print(t)