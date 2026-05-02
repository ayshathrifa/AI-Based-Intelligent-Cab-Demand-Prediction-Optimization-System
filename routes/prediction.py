from flask import Blueprint, request, jsonify
from services.demand_service import predict_demand
from database.db import get_db, log_event
from datetime import datetime

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    required = ['hour', 'day', 'zone', 'weather']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    result = predict_demand(
        hour=data['hour'],
        day=data['day'],
        zone=data['zone'],
        weather=data['weather'],
        temperature=data.get('temperature', 28),
        model_type=data.get('model', 'rf')
    )

    db = get_db()
    db.execute(
        'INSERT INTO predictions (hour, day, zone, weather, temperature, predicted_demand, model_used, created_at) VALUES (?,?,?,?,?,?,?,?)',
        (data['hour'], data['day'], data['zone'], data['weather'],
         data.get('temperature', 28), result['predicted_demand'], data.get('model', 'rf'), datetime.now().isoformat())
    )
    db.commit()
    log_event('INFO', f'Prediction made: zone={data["zone"]}, hour={data["hour"]}, demand={result["predicted_demand"]}, model={data.get("model", "rf")}')
    return jsonify(result), 200

@prediction_bp.route('/stats', methods=['GET'])
def stats():
    db = get_db()
    rows = db.execute('SELECT * FROM predictions ORDER BY id DESC LIMIT 100').fetchall()
    total = sum(r['predicted_demand'] for r in rows) if rows else 1284
    top_zone = max(set(r['zone'] for r in rows), key=lambda z: sum(r['predicted_demand'] for r in rows if r['zone'] == z)) if rows else 'Downtown'
    return jsonify({
        'total_demand': total,
        'peak_hour': '6 PM',
        'active_drivers': 31,
        'top_zone': top_zone
    }), 200
