from flask import Blueprint, jsonify, request
from models.predict_model import predict_demand
from database.db import get_db, log_event
from datetime import datetime

driver_bp = Blueprint('driver', __name__)

ZONES = ['downtown', 'airport', 'suburbs', 'mall', 'hospital', 'university', 'station', 'business_park']

DRIVER_NAMES = [
    'Arjun Sharma', 'Priya Patel', 'Rahul Verma', 'Sneha Nair',
    'Karan Mehta', 'Divya Reddy', 'Amit Singh', 'Pooja Iyer'
]

@driver_bp.route('/allocate', methods=['GET'])
def allocate():
    hour = datetime.now().hour
    day = datetime.now().weekday()
    demands = []
    for zone in ZONES:
        pred = predict_demand(hour=hour, day=day, zone=zone, weather='clear', temperature=28)
        demands.append({'zone': zone, 'demand': pred['predicted_demand'],
                        'recommended_drivers': max(1, pred['predicted_demand'] // 10)})
    demands.sort(key=lambda x: x['demand'], reverse=True)
    return jsonify({'allocations': demands}), 200

@driver_bp.route('/list', methods=['GET'])
def list_drivers():
    db = get_db()
    rows = db.execute('''
        SELECT u.id, u.name, u.email, d.zone, d.status, d.rides_today
        FROM users u
        LEFT JOIN drivers d ON u.id = d.user_id
        WHERE u.role = "driver"
        ORDER BY u.id
    ''').fetchall()
    drivers = []
    for i, r in enumerate(rows):
        drivers.append({
            'id': r['id'],
            'name': r['name'] if r['name'] else DRIVER_NAMES[i % len(DRIVER_NAMES)],
            'email': r['email'],
            'zone': r['zone'] or 'downtown',
            'status': r['status'] or 'Active',
            'rides_today': r['rides_today'] or 0
        })
    return jsonify(drivers), 200

@driver_bp.route('/notify', methods=['POST'])
def notify_driver():
    data = request.get_json()
    user_id = data.get('user_id')
    message = data.get('message')
    new_zone = data.get('zone')
    if not user_id or not message:
        return jsonify({'message': 'user_id and message required'}), 400
    db = get_db()
    db.execute('INSERT INTO notifications (user_id, message) VALUES (?, ?)', (user_id, message))
    if new_zone:
        db.execute('UPDATE drivers SET zone = ? WHERE user_id = ?', (new_zone, user_id))
    db.commit()
    log_event('INFO', f'Notification sent to driver {user_id}: {message}')
    return jsonify({'message': 'Notification sent'}), 200

@driver_bp.route('/notify-all', methods=['POST'])
def notify_all():
    data = request.get_json()
    notifications = data.get('notifications', [])
    db = get_db()
    for n in notifications:
        db.execute('INSERT INTO notifications (user_id, message) VALUES (?, ?)', (n['user_id'], n['message']))
        if n.get('zone'):
            db.execute('UPDATE drivers SET zone = ? WHERE user_id = ?', (n['zone'], n['user_id']))
    db.commit()
    log_event('INFO', f'Bulk allocation applied to {len(notifications)} drivers')
    return jsonify({'message': f'{len(notifications)} drivers notified'}), 200

@driver_bp.route('/notifications/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    db = get_db()
    rows = db.execute(
        'SELECT id, message, is_read, created_at FROM notifications WHERE user_id = ? ORDER BY id DESC LIMIT 20',
        (user_id,)
    ).fetchall()
    return jsonify([dict(r) for r in rows]), 200

@driver_bp.route('/notifications/<int:user_id>/read', methods=['PUT'])
def mark_read(user_id):
    db = get_db()
    db.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (user_id,))
    db.commit()
    return jsonify({'message': 'Marked as read'}), 200

@driver_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    db = get_db()
    user = db.execute('SELECT name, email FROM users WHERE id = ? AND role = ?', (user_id, 'driver')).fetchone()
    if not user:
        return jsonify({'message': 'Driver not found'}), 404
    driver = db.execute('SELECT zone, status, rides_today FROM drivers WHERE user_id = ?', (user_id,)).fetchone()
    if not driver:
        db.execute('INSERT INTO drivers (user_id) VALUES (?)', (user_id,))
        db.commit()
        driver = db.execute('SELECT zone, status, rides_today FROM drivers WHERE user_id = ?', (user_id,)).fetchone()
    hour = datetime.now().hour
    day = datetime.now().weekday()
    pred = predict_demand(hour=hour, day=day, zone=driver['zone'], weather='clear', temperature=28)
    unread = db.execute(
        'SELECT COUNT(*) as cnt FROM notifications WHERE user_id = ? AND is_read = 0', (user_id,)
    ).fetchone()['cnt']
    return jsonify({
        'name': user['name'],
        'email': user['email'],
        'zone': driver['zone'],
        'status': driver['status'],
        'rides_today': driver['rides_today'],
        'zone_demand': pred['predicted_demand'],
        'current_hour': hour,
        'unread_notifications': unread
    }), 200

@driver_bp.route('/profile/<int:user_id>/status', methods=['PUT'])
def update_status(user_id):
    data = request.get_json()
    status = data.get('status')
    if status not in ['Active', 'Idle', 'Offline']:
        return jsonify({'message': 'Invalid status'}), 400
    db = get_db()
    db.execute('UPDATE drivers SET status = ? WHERE user_id = ?', (status, user_id))
    db.commit()
    log_event('INFO', f'Driver {user_id} updated status to {status}')
    return jsonify({'message': 'Status updated'}), 200
