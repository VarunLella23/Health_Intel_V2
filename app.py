from flask import Flask, render_template, request, jsonify
from dashboard import get_fitness_data
from filters import datetimeformat
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
app.jinja_env.filters['datetimeformat'] = datetimeformat

# Load models
diabetes_model = joblib.load('diabetes.pkl')
heart_pipeline = joblib.load('heart_model.pkl')  # Contains complete pipeline

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
            # Get input data
            data = request.get_json() if request.is_json else request.form.to_dict()
            
            # Create DataFrame with explicit type conversion
            input_df = pd.DataFrame([{
                # Numerical features
                'age': float(data.get('age', 0)),
                'trestbps': float(data.get('trestbps', 0)),
                'chol': float(data.get('chol', 0)),
                'thalach': float(data.get('thalach', 0)),
                'oldpeak': float(data.get('oldpeak', 0)),
                
                # Categorical features
                'sex': int(data.get('sex', 0)),
                'cp': int(data.get('cp', 0)),
                'fbs': int(data.get('fbs', 0)),
                'restecg': int(data.get('restecg', 0)),
                'exang': int(data.get('exang', 0)),
                'slope': int(data.get('slope', 0)),
                'ca': int(data.get('ca', 0)),
                'thal': int(data.get('thal', 0))
            }])

            # Ensure correct column order
            input_df = input_df[[
                'age', 'trestbps', 'chol', 'thalach', 'oldpeak',
                'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'
            ]]

            # Make prediction
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)