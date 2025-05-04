from flask import Flask, render_template, request, jsonify
from flask import abort
from dashboard import get_fitness_data
from filters import datetimeformat
import pandas as pd
import numpy as np
import joblib
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ['FLASK_SECRET_KEY','dev-secret-key'],
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=3600
)

app = Flask(__name__)
app.jinja_env.filters['datetimeformat'] = datetimeformat

MODELS = {
    'diabetes': joblib.load('diabetes.pkl'),
    'heart': joblib.load('heart_model.pkl'),
    'lungs': joblib.load('lungs.pkl'),
    'liver': joblib.load('liver.pkl')
}

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/dashboard')
def dashboard():
    fitness_data = get_fitness_data()
    return render_template(
        'dashboard.html',
        metrics=fitness_data.get('metrics', {}),
        time_range=fitness_data.get('time_range', {}),
        success=fitness_data.get('success', False),
        error=fitness_data.get('error', None)
    )

@app.route('/dashboard')
def dashbaord():
    return render_template('dashboard.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

def handle_prediction_error(model_name, error):
    app.logger.error(f'{model_name} prediction error: {str(error)}')
    return jsonify({'error': f'{model_name} prediction failed', 'details': str(error)}), 500

# Diabetes Prediction
@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'POST':
        try:
            features = [float(request.form[col]) for col in [
                'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
            
            prediction = MODELS['diabetes'].predict([features])[0]
            return "Diabetic" if prediction == 1 else "Not Diabetic"
        
        except Exception as e:
            return handle_prediction_error('Diabetes', e)
    return render_template('diabetes.html')

# Heart Disease Prediction
@app.route('/heart', methods=['GET', 'POST'])
def heart_prediction():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            input_df = pd.DataFrame([{
                'age': float(data.get('age', 0)),
                'trestbps': float(data.get('trestbps', 0)),
                'chol': float(data.get('chol', 0)),
                'thalach': float(data.get('thalach', 0)),
                'oldpeak': float(data.get('oldpeak', 0)),
                'sex': int(data.get('sex', 0)),
                'cp': int(data.get('cp', 0)),
                'fbs': int(data.get('fbs', 0)),
                'restecg': int(data.get('restecg', 0)),
                'exang': int(data.get('exang', 0)),
                'slope': int(data.get('slope', 0)),
                'ca': int(data.get('ca', 0)),
                'thal': int(data.get('thal', 0))
            }])

            prediction = MODELS['heart'].predict(input_df)[0]
            return jsonify({'prediction': 'High Risk' if prediction == 1 else 'Low Risk'})

        except Exception as e:
            return handle_prediction_error('Heart', e)
    
    return render_template('heart.html')

# Liver Disease Prediction (New)
@app.route('/liver', methods=['GET', 'POST'])
def liver_prediction():
    if request.method == 'POST':
        try:
            features = [
                float(request.form['Age']),
                float(request.form['Gender']),
                float(request.form['BMI']),
                float(request.form['Alcohol']),
                float(request.form['Smoking']),
                float(request.form['GeneticRisk']),
                float(request.form['PhysicalActivity']),
                float(request.form['Diabetes']),
                float(request.form['Hypertension']),
                float(request.form['LiverFunction'])
            ]
            
            prediction = MODELS['liver'].predict([features])[0]
            return "High Risk" if prediction == 1 else "Low Risk"
        
        except Exception as e:
            return handle_prediction_error('Liver', e)
    
    return render_template('liver.html')

# Lung Disease Prediction
@app.route('/lungs', methods=['GET', 'POST'])
def lung_prediction():
    if request.method == 'POST':
        try:
            data = request.get_json()
            input_df = pd.DataFrame([{
                'YELLOW_FINGERS': int(data.get('YELLOW_FINGERS', 0)),
                'ANXIETY': int(data.get('ANXIETY', 0)),
                'PEER_PRESSURE': int(data.get('PEER_PRESSURE', 0)),
                'CHRONIC DISEASE': int(data.get('CHRONIC_DISEASE', 0)),
                'FATIGUE ': int(data.get('FATIGUE ', 0)),
                'ALLERGY ': int(data.get('ALLERGY ', 0)),
                'WHEEZING': int(data.get('WHEEZING', 0)),
                'ALCOHOL CONSUMING': int(data.get('ALCOHOL_CONSUMING', 0)),
                'COUGHING': int(data.get('COUGHING', 0)),
                'SWALLOWING DIFFICULTY': int(data.get('SWALLOWING_DIFFICULTY', 0)),
                'CHEST PAIN': int(data.get('CHEST_PAIN', 0)),
                'ANXYELFIN': int(data.get('ANXIETY', 0)) * int(data.get('YELLOW_FINGERS', 0))
            }])

            prediction = MODELS['lungs'].predict(input_df)[0]
            return jsonify({"prediction": "High Risk" if prediction == 1 else "Low Risk"})

        except Exception as e:
            return handle_prediction_error('Lung', e)
    
    return render_template('lungs.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))