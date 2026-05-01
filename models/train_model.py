import os, pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from utils.preprocessing import preprocess_data

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset')

def train_model(model_type='rf', dataset='cab_data.csv', test_split=0.2, n_estimators=100):
    path = os.path.join(DATASET_DIR, dataset)
    if not os.path.exists(path):
        return {'error': f'Dataset {dataset} not found'}

    df = pd.read_csv(path)
    X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_split, random_state=42)

    models_to_train = ['rf', 'lr'] if model_type == 'both' else [model_type]
    results = {}

    for mt in models_to_train:
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=42) if mt == 'rf' else LinearRegression()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mae = round(mean_absolute_error(y_test, preds), 2)
        r2 = round(r2_score(y_test, preds), 3)
        accuracy = round(max(0, r2) * 100, 1)

        model_path = os.path.join(MODEL_DIR, f'{"rf" if mt == "rf" else "lr"}_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        results[mt] = {'accuracy': accuracy, 'mae': mae, 'r2': r2}

    return results.get(model_type, results)
