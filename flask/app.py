from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import pickle
import schedule
import time
import numpy as np
from model import upbit_api, model_prediction
from database import mysql_connection
from datetime import datetime

app = Flask(__name__)

model = tf.keras.models.load_model("./save.h5")

def collect_and_predict():
    data = upbit_api()  # 데이터 수집
    prediction = model_prediction(data)  # 데이터로 예측
    connection = mysql_connection(prediction)



def job():
    print("데이터 수집 및 예측 시작")
    collect_and_predict()
    print("데이터 수집 및 예측 완료")

if __name__ == "__main__":
    app.run(debug=True)

    while True:
        schedule.run_pending()
        time.sleep(1)
'''
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form['date']
    prediction = model_prediction(data)  # 데이터로 예측

    return render_template('visualization.html', prediction=prediction)
'''