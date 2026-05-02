from flask import Blueprint, request, jsonify
from models.train_model import train_model
from database.db import log_event

train_bp = Blueprint('train', __name__)

@train_bp.route('', methods=['POST'])
def train():
    data = request.get_json()
    model_type = data.get('model', 'rf')
    dataset = data.get('dataset', 'cab_data.csv')
    test_split = data.get('test_split', 0.2)
    n_estimators = data.get('n_estimators', 100)

    result = train_model(model_type=model_type, dataset=dataset,
                         test_split=test_split, n_estimators=n_estimators)
    log_event('INFO', f'Model trained: {model_type.upper()} on {dataset} — accuracy={result.get("accuracy", "N/A")}')
    return jsonify(result), 200
