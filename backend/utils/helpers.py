from datetime import datetime
from functools import wraps
from flask import request, jsonify

def get_time_period(hour):
    if hour < 6: return 'night'
    if hour < 12: return 'morning'
    if hour < 17: return 'afternoon'
    if hour < 21: return 'evening'
    return 'night'

def is_peak_hour(hour):
    return (7 <= hour <= 9) or (17 <= hour <= 20)

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        from database.db import get_db
        user = get_db().execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

def format_response(data, message='Success', status=200):
    return jsonify({'status': 'success', 'message': message, 'data': data}), status
