from flask import Flask, send_file, request, jsonify
import joblib
import numpy as np
import sqlite3
import pandas as pd
import json
from datetime import datetime

app = Flask(__name__)

# Load the trained Random Forest model
model = joblib.load('random_forest_model.joblib')

# Feature names for reference (must match keys expected in JSON/form)
FEATURE_NAMES = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
                 'insulin', 'bmi', 'diabetes_pedigree', 'age']


def create_database():
    """Create SQLite database and table if not exists (id is auto-increment integer)."""
    conn = sqlite3.connect('diabetes.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diabetes_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregnancies INTEGER NOT NULL,
            glucose INTEGER NOT NULL,
            blood_pressure INTEGER NOT NULL,
            skin_thickness INTEGER NOT NULL,
            insulin INTEGER NOT NULL,
            bmi REAL NOT NULL,
            diabetes_pedigree REAL NOT NULL,
            age INTEGER NOT NULL,
            outcome INTEGER DEFAULT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def preprocess_data(data):
    """Preprocess input data for model prediction"""
    # data can be dict or list; ensure order matches FEATURE_NAMES
    if isinstance(data, list):
        features = np.array(data).reshape(1, -1)
    else:
        features = np.array([data[col] for col in FEATURE_NAMES]).reshape(1, -1)
    return features


def predict_diabetes(features):
    """Make prediction using the loaded Random Forest model"""
    predicted_class = int(model.predict(features)[0])

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(features)[0][1])
    else:
        probability = float(predicted_class)  # fallback

    return {
        'prediction': predicted_class,
        'probability': probability,
        'risk_level': 'High' if predicted_class == 1 else 'Low'
    }


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/manual_inference', methods=['POST'])
def manual_inference():
    try:
        data = {
            'pregnancies': int(float(request.form.get('pregnancies', 0))),
            'glucose': int(float(request.form.get('glucose', 0))),
            'blood_pressure': int(float(request.form.get('blood_pressure', 0))),
            'skin_thickness': int(float(request.form.get('skin_thickness', 0))),
            'insulin': int(float(request.form.get('insulin', 0))),
            'bmi': float(request.form.get('bmi', 0)),
            'diabetes_pedigree': float(request.form.get('diabetes_pedigree', 0)),
            'age': int(float(request.form.get('age', 0)))
        }

        features = preprocess_data(data)
        result = predict_diabetes(features)

        result['input_data'] = data
        result['method'] = 'Manual Input'

        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/sql_inference', methods=['POST'])
def sql_inference():
    try:
        record_id = request.form.get('record_id')
        if not record_id:
            return jsonify({'success': False, 'error': 'Record ID is required'}), 400

        # convert to int if possible (we expect numeric auto-increment id)
        try:
            record_id_int = int(record_id)
        except ValueError:
            return jsonify({'success': False, 'error': 'Record ID must be an integer'}), 400

        conn = sqlite3.connect('diabetes.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pregnancies, glucose, blood_pressure, skin_thickness,
                   insulin, bmi, diabetes_pedigree, age
            FROM diabetes_records
            WHERE id = ?
        ''', (record_id_int,))
        record = cursor.fetchone()
        conn.close()

        if not record:
            return jsonify({'success': False, 'error': 'Record not found'}), 404

        data = {
            'pregnancies': int(record[0]),
            'glucose': int(record[1]),
            'blood_pressure': int(record[2]),
            'skin_thickness': int(record[3]),
            'insulin': int(record[4]),
            'bmi': float(record[5]),
            'diabetes_pedigree': float(record[6]),
            'age': int(record[7])
        }

        features = preprocess_data(list(record))
        result = predict_diabetes(features)

        result['input_data'] = data
        result['method'] = 'SQL Query'
        result['record_id'] = record_id_int

        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/inference', methods=['POST'])
def api_inference():
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'JSON data is required'}), 400

        missing_fields = [field for field in FEATURE_NAMES if field not in data]
        if missing_fields:
            return jsonify({'success': False, 'error': f'Missing required fields: {missing_fields}'}), 400

        features = preprocess_data(data)
        result = predict_diabetes(features)

        result['input_data'] = data
        result['method'] = 'API'

        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/load_sample_data', methods=['POST'])
def load_sample_data():
    """
    Load sample rows from diabetes.csv into SQLite.
    IMPORTANT: with AUTOINCREMENT id, we do NOT insert id explicitly.
    """
    try:
        df = pd.read_csv('diabetes.csv')
        conn = sqlite3.connect('diabetes.db')
        cursor = conn.cursor()

        # Optional: clear existing records first
        cursor.execute('DELETE FROM diabetes_records')

        # If you want to reset autoincrement counter in SQLite:
        # cursor.execute("DELETE FROM sqlite_sequence WHERE name='diabetes_records'")

        # Insert first N rows (here head(10))
        for _, row in df.head(10).iterrows():
            cursor.execute('''
                INSERT INTO diabetes_records
                (pregnancies, glucose, blood_pressure, skin_thickness,
                 insulin, bmi, diabetes_pedigree, age, outcome, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                int(row['Pregnancies']),
                int(row['Glucose']),
                int(row['BloodPressure']),
                int(row['SkinThickness']),
                int(row['Insulin']),
                float(row['BMI']),
                float(row['DiabetesPedigreeFunction']),
                int(row['Age']),
                int(row['Outcome']),
                datetime.now()
            ))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Sample data loaded successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/get_records')
def get_records():
    try:
        conn = sqlite3.connect('diabetes.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, pregnancies, glucose, blood_pressure, skin_thickness,
                   insulin, bmi, diabetes_pedigree, age, outcome, created_at
            FROM diabetes_records
            ORDER BY created_at DESC
        ''')
        records = cursor.fetchall()
        conn.close()

        formatted_records = []
        for record in records:
            formatted_records.append({
                'id': record[0],
                'pregnancies': record[1],
                'glucose': record[2],
                'blood_pressure': record[3],
                'skin_thickness': record[4],
                'insulin': record[5],
                'bmi': record[6],
                'diabetes_pedigree': record[7],
                'age': record[8],
                'outcome': record[9],
                'created_at': record[10]
            })

        return jsonify({'success': True, 'records': formatted_records})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    create_database()
    print("🚀 Diabetes Prediction App Starting...")
    print("📊 Random Forest model loaded successfully!")
    print("🔗 Access the app at: http://localhost:3001")
    app.run(debug=True, host='0.0.0.0', port=3001)
