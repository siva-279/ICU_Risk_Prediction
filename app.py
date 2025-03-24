import pandas as pd
from flask import Flask, render_template, jsonify, request
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the ICU risk classified dataset
data_file = "icu_risk_classified.csv"

def load_data():
    return pd.read_csv(data_file)

patient_data = load_data()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/icu_trends')
def icu_trends():
    return render_template('icu_trends.html')

@app.route('/risk_classification')
def risk_classification():
    return render_template('risk_classification.html', patients=patient_data.to_dict(orient="records"))

@app.route('/resource_forecasting')
def resource_forecasting():
    return render_template('resource_forecasting.html')

@app.route('/api/get_risk_data', methods=['GET'])
def get_risk_data():
    return jsonify(patient_data.to_dict(orient="records"))

@app.route('/api/get_icu_trends', methods=['GET'])
def get_icu_trends():
    days = int(request.args.get('days', 30))
    condition = request.args.get('condition', 'All')

    def generate_icu_trends(days=30, condition="All"):
        date_list = [(datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        icu_data = []

        for date in date_list:
            icu_data.append({
                "date": date,
                "admissions": random.randint(5, 20),
                "condition": condition if condition != "All" else random.choice(["Sepsis", "COVID-19", "Pneumonia"]),
                "day_of_week": datetime.strptime(date, "%Y-%m-%d").strftime("%A")
            })

        return icu_data

    icu_data = generate_icu_trends(days, condition)
    return jsonify(icu_data)

@app.route('/api/get_resource_forecast', methods=['GET'])
def get_resource_forecast():
    range_days = int(request.args.get("range", 30))

    def generate_forecasting_data(days=30):
        forecast_data = []
        start_date = datetime.today()

        for i in range(days):
            date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            forecast_data.append({
                "date": date,
                "icu_beds": random.randint(10, 30),
                "ventilators": random.randint(5, 15),
                "medications": random.randint(50, 150)
            })

        return forecast_data

    forecast_data = generate_forecasting_data(range_days)
    return jsonify(forecast_data)

if __name__ == '__main__':
    app.run(debug=True)
