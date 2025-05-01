from flask import Flask, render_template, request, jsonify
from flask import abort
from dashboard import get_fitness_data
from filters import datetimeformat
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)
app.jinja_env.filters['datetimeformat'] = datetimeformat

# Load models
diabetes_model = joblib.load('diabetes.pkl')
heart_pipeline = joblib.load('heart_model.pkl')
lung_model = joblib.load('lungs.pkl')    

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

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'POST':
        try:
            features = [float(request.form[col]) for col in [
                'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]

            prediction = diabetes_model.predict([features])[0]
            return "Diabetic" if prediction == 1 else "Not Diabetic"
        
        except Exception as e:
            app.logger.error(f'Diabetes prediction error: {str(e)}')
            return "Error processing request", 500
    return render_template('diabetes.html')

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

            input_df = input_df[[
                'age', 'trestbps', 'chol', 'thalach', 'oldpeak',
                'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'
            ]]

            prediction = heart_pipeline.predict(input_df)[0]

            return jsonify({
                'prediction': 'High Risk' if prediction == 1 else 'Low Risk',
                'status': 'success'
            })

        except Exception as e:
            return jsonify({
                'error': f'Prediction failed: {str(e)}',
                'status': 'error'
            }), 400

    return render_template('heart.html')
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
                'FATIGUE ': int(data.get('FATIGUE ', 0)),  # Trailing space
                'ALLERGY ': int(data.get('ALLERGY ', 0)),    # Trailing space
                'WHEEZING': int(data.get('WHEEZING', 0)),
                'ALCOHOL CONSUMING': int(data.get('ALCOHOL_CONSUMING', 0)),
                'COUGHING': int(data.get('COUGHING', 0)),
                'SWALLOWING DIFFICULTY': int(data.get('SWALLOWING_DIFFICULTY', 0)),
                'CHEST PAIN': int(data.get('CHEST_PAIN', 0)),
                'ANXYELFIN': int(data.get('ANXIETY', 0)) * int(data.get('YELLOW_FINGERS', 0))
            }])

            # Maintain exact column order
            input_df = input_df[[
                'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE',
                'FATIGUE ', 'ALLERGY ', 'WHEEZING', 'ALCOHOL CONSUMING',  # Trailing spaces
                'COUGHING', 'SWALLOWING DIFFICULTY', 'CHEST PAIN', 'ANXYELFIN'
            ]]

            prediction = lung_model.predict(input_df)[0]
            return jsonify({
                "prediction": "High Risk" if prediction == 1 else "Low Risk",
                "status": "success"
            })

        except Exception as e:
            return jsonify({
                "error": f"Prediction failed: {str(e)}",
                "status": "error"
            }), 400
    
    # Serve form for GET requests
    return render_template('lungs.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
