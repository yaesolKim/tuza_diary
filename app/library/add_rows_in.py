import datetime

import numpy as np
import pandas as pd
import psycopg2  # db driver
import FinanceDataReader as fdr
import pyupbit


def create_training_engine():
    conn = psycopg2.connect(dbname="y_tuza_diary", user="postgres", password="yaesol", host="localhost", port="5432")
    return conn


class DataNotEnough(BaseException):
    pass


def get_table_list():
    engine = create_training_engine()
    sql = f"""SELECT table_name 
                FROM information_schema.tables"""
    df_tables = pd.read_sql(sql, engine)
    return df_tables


def add_market(table_name="app_market"):
    engine = create_training_engine()
    cursor = engine.cursor()

    sql = f"""INSERT INTO {table_name} (name, code)
    VALUES ('국내주식', 'a'), ('해외주식', 'b'), ('코인', 'KRW');"""

    cursor.execute(sql)
    engine.commit()
    cursor.close()
    engine.close()


def add_candle(market_id, table_name="app_candle"):
    engine = create_training_engine()
    cursor = engine.cursor()
    values = ""

    if market_id == 1:
        df_kr = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
        for i in range(len(df_kr)):
            # df_kr['종목코드'][i] 0 채워넣어주  SELECT lpad(df_kr['종목코드'][i], 6, '0');
            values += f"(lpad('{df_kr['종목코드'][i]}', 6, '0'), '{df_kr['회사명'][i]}', {market_id}),"
    elif market_id == 2:
        df_nasdaq = fdr.StockListing('NASDAQ')
        for i in range(len(df_nasdaq)):
            code_name = df_nasdaq['Name'][i].replace("'", "_")[:50]
            values += f"('{df_nasdaq['Symbol'][i]}', '{code_name}', {market_id}),"
    elif market_id == 3:
        tickers = pyupbit.get_tickers()
        for code in tickers:
            values += f"('{code}', '{code}', {market_id}),"

    values = values[:-1]
    sql = f"""INSERT INTO {table_name} (code, code_name, market_id)
    VALUES {values};"""
    cursor.execute(sql)
    engine.commit()
    cursor.close()
    engine.close()


if __name__ == "__main__":
    option = int(input(f"""원하는 동작 입력:
1. market 데이터 추가 
2. candle 데이터 추가 
3. 
9. 테이블 리스트 
"""))

    if option == 1:
        add_market()
    elif option == 2:
        market_id = int(input(f"market_id 입력: (1:국내주식, 2:해외주식, 3:코인)"))
        add_candle(market_id=market_id)
    elif option == 9:
        get_table_list()
