import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset')
MODEL_DIR   = os.path.join(os.path.dirname(__file__))

ZONE_MAP    = {'downtown': 0, 'airport': 1, 'suburbs': 2, 'mall': 3,
               'hospital': 4, 'university': 5, 'station': 6, 'business_park': 7, 'old_city': 8}
WEATHER_MAP = {'clear': 0, 'cloudy': 1, 'rain': 2, 'heavy_rain': 3, 'fog': 4}

def train_model(model_type='rf', dataset='cab_data.csv', test_split=0.2, n_estimators=100):
    path = os.path.join(DATASET_DIR, dataset)
    if not os.path.exists(path):
        return {'error': f'Dataset {dataset} not found'}

    df = pd.read_csv(path)

    # encode string columns if present
    if df['zone'].dtype == object:
        df['zone'] = df['zone'].map(ZONE_MAP).fillna(0).astype(int)
    if df['weather'].dtype == object:
        df['weather'] = df['weather'].map(WEATHER_MAP).fillna(0).astype(int)

    feature_cols = ['hour', 'day_of_week', 'zone', 'weather', 'temperature']
    target_col   = 'demand'

    missing = [c for c in feature_cols + [target_col] if c not in df.columns]
    if missing:
        return {'error': f'Missing columns: {missing}'}

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=42)

    if model_type == 'rf':
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42)
    else:
        model = LinearRegression()

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae      = round(mean_absolute_error(y_test, preds), 2)
    r2       = round(r2_score(y_test, preds), 4)
    accuracy = round(max(0, r2) * 100, 1)

    save_path = os.path.join(MODEL_DIR, f'{model_type}_model.pkl')
    with open(save_path, 'wb') as f:
        pickle.dump(model, f)

    return {
        'message': f'{model_type.upper()} model trained successfully',
        'accuracy': accuracy,
        'r2': r2,
        'mae': mae,
        'samples': len(df),
        'model_type': model_type
    }
