from flask import Flask, render_template, request, send_from_directory
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pickle
import pandas as pd
import os

app = Flask(__name__, static_folder='static')

model_path = 'model/model.sav'
csv_path = 'winequality-red.csv'

if not os.path.isfile(model_path):
    raise Exception(f"Model file not found at {model_path}")
if not os.path.isfile(csv_path):
    raise Exception(f"CSV file not found at {csv_path}")

Wine_model = pickle.load(open(model_path, 'rb'))


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chatbot/app.py')
def chatbot():
    return render_template('app.py')

@app.route('/templates/shop.html')
def shop():
    images = [f for f in os.listdir('static/img') if f.endswith('.jpg') or f.endswith('.png')]
    return render_template('shop.html', images=images)



# Route to serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/static/img/<path:path>')
def send_image(path):
    return send_from_directory('static/img', path)

@app.route('/static/css/style.css')
def css():
    return app.send_static_file('css/style.css')

@app.route('/predict', methods=['POST'])
def predict():
    fixed_acidity = request.form.get('fixed_acidity', type=float)
    volatile_acidity = request.form.get('volatile_acidity', type=float)
    citric_acid = request.form.get('citric_acid', type=float)
    residual_sugar = request.form.get('residual_sugar', type=float)
    chlorides = request.form.get('chlorides', type=float)
    free_sulfur_dioxide = request.form.get('free_sulfur_dioxide', type=float)
    total_sulfur_dioxide = request.form.get('total_sulfur_dioxide', type=float)
    density = request.form.get('density', type=float)
    pH = request.form.get('pH', type=float)
    sulphates = request.form.get('sulphates', type=float)
    alcohol = request.form.get('alcohol', type=float)

    # Check if any of the fields are empty
    if None in[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
               free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]:
        return render_template('home.html', error_msg='Please fill in all the fields.')

    # Load the dataset and scale the input data
    dataset = pd.read_csv('winequality-red.csv')
    dataset_X = dataset.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]].values
    sc = MinMaxScaler(feature_range=(0, 1))
    dataset_scaled = sc.fit_transform(dataset_X)

    input_data = [[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                   free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]]
    transformed_data = sc.transform(input_data)

    # Load the model and make a prediction
    Wine_model = pickle.load(open('model/model.sav', 'rb'))
    prediction = Wine_model.predict(transformed_data)

    # Check the prediction and show the appropriate template
    if prediction == 0:
        msg = 'Good quality wine'
        return render_template('goodwine.html', prediction=msg, input_data=input_data[0])
    else:
        msg = 'Bad quality wine'
        return render_template('badwine.html', prediction=msg, input_data=input_data[0])

if __name__ == '__main__':
    app.run(debug=True)
