import os
import pickle

model_path = os.path.join("models", "lr_model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

def predict_demand(hour, day, zone, weather, temperature):
    # Example input (modify based on your model)
    features = [[hour, day, temperature]]

    prediction = model.predict(features)

    return {
        "predicted_demand": int(prediction[0])
    }
from datetime import datetime

ZONES = ['downtown', 'airport', 'suburbs', 'mall', 'hospital', 'university', 'station', 'business_park', 'old_city']

def get_all_zone_demands(weather='clear', temperature=28):
    now = datetime.now()
    results = []
    for zone in ZONES:
        pred = predict_demand(hour=now.hour, day=now.weekday(), zone=zone,
                              weather=weather, temperature=temperature)
        results.append({'zone': zone, 'demand': pred['predicted_demand']})
    return sorted(results, key=lambda x: x['demand'], reverse=True)

def get_demand_trend(zone, hours=24):
    now = datetime.now()
    trend = []
    for h in range(hours):
        pred = predict_demand(hour=h, day=now.weekday(), zone=zone, weather='clear', temperature=28)
        trend.append({'hour': h, 'demand': pred['predicted_demand']})
    return trend
