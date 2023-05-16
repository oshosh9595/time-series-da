from sqlalchemy import create_engine
import pymysql
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz

# 데이터 저장을 위한 MySQL 연결 설정
db_connection_str = 'mysql+pymysql://root:1234@localhost:3306/bitcoin'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

# 데이터를 가져올 시작 날짜와 종료 날짜 설정
start_date = datetime.now(pytz.utc)
end_date = datetime(2017, 9, 25, tzinfo=pytz.utc)

# 데이터를 가져올 페이지 수 계산
delta = start_date - end_date
num_pages = delta.days // 200 + 1

# 데이터를 가져와서 MySQL에 저장
for page in range(num_pages):
    url = f"https://api.upbit.com/v1/candles/minutes/5?market=KRW-BTC&count=200&to={start_date}&page={page + 1}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    df_bitcoin = pd.DataFrame(data, columns=['candle_date_time_utc', 'candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_price', 'candle_acc_trade_volume'])
    
    # 타임존 변환
    df_bitcoin['candle_date_time_utc'] = pd.to_datetime(df_bitcoin['candle_date_time_kst']).dt.tz_localize('Asia/Seoul').dt.tz_convert('UTC')
    
    df_bitcoin.to_sql(name='apidata', con=db_connection, if_exists='append', index=False)
    
    # 다음 페이지를 위해 시작 날짜 업데이트
    start_date -= timedelta(days=200)
