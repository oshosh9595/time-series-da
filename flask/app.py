from flask import Flask, render_template, request
import tensorflow as tf
import pickle
import numpy as np
from model import visualization

app = Flask(__name__)
#tf.compat.v1.disable_eager_execution()

#저장된 모델 가져오기
'''
saver = tf.train.Saver()
model = tf.compat.v1.global_variables_initializer()

sess = tf.Session()
sess.run(model)

save_path = "./model.py/save.h5"
saver.restore(sess, save_path)
'''
model = tf.keras.models.load_model("./save.h5")
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html') #get 시 index.html 보여주기
    if request.method == 'POST':
        date = request.form['date']
        #ohours = float(request.form['1hours'])
        #fhours = float(request.form['1hours'])
        #day = float(request.form['day'])

        prediction = 0

        #사용자가 가져온 데이터 2차원으로 만들기
        #data = ((date, ohours, fhours, day), )
        data = ((date),)
        arr = np.array(data, dtype=np.float32)

        #x_data = np.array([[date, ohours, fhours, day]], dtype=np.float32)
        x_data = np.zeros((1, 24, 6), dtype=np.float32)
        x_data[0, 0, 0] = date
        y_pred = model.predict(x_data)

        prediction = y_pred[0]
        return render_template('visualization.html', prediction=prediction, visualization=visualization)
    
if __name__ == "__main__":
    app.run(debug=True)