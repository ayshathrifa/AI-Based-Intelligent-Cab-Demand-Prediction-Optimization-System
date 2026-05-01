import os, pickle
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split
from utils.preprocessing import preprocess_data
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'dataset')

def compare_models(dataset='cab_data.csv'):
    path = os.path.join(DATASET_DIR, dataset)
    if not os.path.exists(path):
        return {'error': 'Dataset not found'}

    df = pd.read_csv(path)
    X, y = preprocess_data(df)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    results = {}
    for mt in ['rf', 'lr']:
        model_path = os.path.join(MODEL_DIR, f'{mt}_model.pkl')
        if not os.path.exists(model_path):
            continue
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        preds = model.predict(X_test)
        results[mt] = {
            'mae': round(mean_absolute_error(y_test, preds), 2),
            'rmse': round(np.sqrt(mean_squared_error(y_test, preds)), 2),
            'r2': round(r2_score(y_test, preds), 3),
            'accuracy': round(max(0, r2_score(y_test, preds)) * 100, 1)
        }
    return results
