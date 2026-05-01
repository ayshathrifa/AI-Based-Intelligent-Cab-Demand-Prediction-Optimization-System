from flask import Blueprint, jsonify, request
from database.db import get_db, log_event
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/logs', methods=['GET'])
def get_logs():
    db = get_db()
    rows = db.execute('SELECT level, message, created_at FROM logs ORDER BY id DESC LIMIT 50').fetchall()
    return jsonify([dict(r) for r in rows]), 200

@admin_bp.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    rows = db.execute('SELECT id, name, email, role, created_at FROM users ORDER BY id DESC').fetchall()
    return jsonify([dict(r) for r in rows]), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    role = data.get('role')
    db = get_db()
    user = db.execute('SELECT id, email FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.execute('UPDATE users SET role = ? WHERE id = ?', (role, user_id))
    db.commit()
    log_event('INFO', f'Admin updated user {user["email"]} role to {role}')
    return jsonify({'message': 'User updated'}), 200

@admin_bp.route('/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    if not all([name, email, subject, message]):
        return jsonify({'message': 'All fields are required'}), 400
    db = get_db()
    db.execute('INSERT INTO contact_messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
               (name, email, subject, message))
    db.commit()
    log_event('INFO', f'Contact message from {name} ({email}): {subject}')
    return jsonify({'message': 'Message received'}), 201

@admin_bp.route('/contact', methods=['GET'])
def get_contact_messages():
    db = get_db()
    rows = db.execute('SELECT id, name, email, subject, message, created_at FROM contact_messages ORDER BY id DESC').fetchall()
    return jsonify([dict(r) for r in rows]), 200
