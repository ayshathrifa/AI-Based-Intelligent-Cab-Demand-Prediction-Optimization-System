from flask import Blueprint, jsonify
from models.predict_model import predict_demand
from datetime import datetime

realtime_bp = Blueprint('realtime', __name__)

@realtime_bp.route('/predict', methods=['GET'])
def realtime_predict():
    now = datetime.now()
    result = predict_demand(hour=now.hour, day=now.weekday(), zone='downtown', weather='clear', temperature=28)
    result['timestamp'] = now.isoformat()
    return jsonify(result), 200
