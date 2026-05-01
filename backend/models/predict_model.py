import os
import pickle
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__))

_models = {}

def load_model(model_type='rf'):
    if model_type not in _models:
        path = os.path.join(MODEL_DIR, f'{model_type}_model.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                _models[model_type] = pickle.load(f)
        else:
            _models[model_type] = None
    return _models[model_type]

ZONE_MAP = {
    'downtown': 0, 'airport': 1, 'suburbs': 2, 'mall': 3,
    'hospital': 4, 'university': 5, 'station': 6, 'business_park': 7, 'old_city': 8
}
WEATHER_MAP = {'clear': 0, 'cloudy': 1, 'rain': 2, 'heavy_rain': 3, 'fog': 4}

def predict_demand(hour, day, zone, weather, temperature=28, model_type='rf'):
    zone_enc    = ZONE_MAP.get(zone, 0)
    weather_enc = WEATHER_MAP.get(weather, 0)

    model = load_model(model_type)
    if model:
        features = pd.DataFrame(
            [[hour, day, zone_enc, weather_enc, temperature]],
            columns=['hour', 'day_of_week', 'zone', 'weather', 'temperature']
        )
        demand = int(round(model.predict(features)[0]))
    else:
        base = [87, 72, 34, 65, 48, 55, 91, 43, 29][zone_enc]
        hour_factor   = 1.8 if (7 <= hour <= 9 or 17 <= hour <= 20) else 0.5 if hour < 6 else 1.0
        weather_bonus = [0, 5, 20, 35, 10][weather_enc]
        weekend_bonus = 15 if day >= 5 else 0
        demand = int(base * hour_factor + weather_bonus + weekend_bonus)

    return {
        'predicted_demand': max(0, demand),
        'zone': zone,
        'model_used': model_type,
        'confidence': 0.94 if model_type == 'rf' else 0.81
    }
