from flask import Blueprint, jsonify

insights_bp = Blueprint('insights', __name__)

@insights_bp.route('/', methods=['GET'])
def get_insights():
    insights = [
        {'title': 'Weekend demand is higher', 'detail': 'Weekend cab demand is 40% higher than weekdays', 'impact': 'High'},
        {'title': 'Rain increases demand', 'detail': 'Rainy weather causes 25-35% surge in demand', 'impact': 'High'},
        {'title': 'Office hours drive demand', 'detail': 'Business zones see 3x demand during 8-10 AM and 5-7 PM', 'impact': 'Medium'},
        {'title': 'Airport demand is consistent', 'detail': 'Airport zone maintains steady demand 24/7', 'impact': 'Medium'},
        {'title': 'Holidays cause demand spikes', 'detail': 'Public holidays show 60% higher demand in entertainment zones', 'impact': 'Critical'},
    ]
    return jsonify({'insights': insights}), 200
