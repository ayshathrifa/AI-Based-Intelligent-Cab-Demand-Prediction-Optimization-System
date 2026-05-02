from flask import Blueprint, jsonify, request
from models.predict_model import predict_demand
from datetime import datetime

zones_bp = Blueprint('zones', __name__)

ZONES = ['downtown', 'airport', 'suburbs', 'mall', 'hospital', 'university', 'station', 'business_park', 'old_city']

@zones_bp.route('/', methods=['GET'])
def get_zones():
    hour = int(request.args.get('hour', datetime.now().hour))
    day = int(request.args.get('day', datetime.now().weekday()))
    weather = request.args.get('weather', 'clear')
    results = []
    for zone in ZONES:
        pred = predict_demand(hour=hour, day=day, zone=zone, weather=weather, temperature=28)
        results.append({'zone': zone, 'demand': pred['predicted_demand']})
    results.sort(key=lambda x: x['demand'], reverse=True)
    return jsonify(results), 200
