from flask import Blueprint, request, jsonify
from database.db import get_db, log_event
import hashlib, secrets

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name, email, password, role = data.get('name'), data.get('email'), data.get('password'), data.get('role', 'user')
    if not all([name, email, password]):
        return jsonify({'message': 'All fields required'}), 400
    db = get_db()
    if db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone():
        return jsonify({'message': 'Email already registered'}), 409
    db.execute('INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
               (name, email, hash_password(password), role))
    db.commit()
    log_event('INFO', f'New user registered: {email} as {role}')
    return jsonify({'message': 'Account created successfully'}), 201

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email')
    db = get_db()
    user = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    if user:
        return jsonify({'message': 'Email found'}), 200
    return jsonify({'message': 'Email not found'}), 404

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    if not email or not new_password:
        return jsonify({'message': 'Missing fields'}), 400
    db = get_db()
    user = db.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
    if not user:
        return jsonify({'message': 'Email not found'}), 404
    db.execute('UPDATE users SET password = ? WHERE email = ?', (hash_password(new_password), email))
    db.commit()
    return jsonify({'message': 'Password reset successful'}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password, role = data.get('email'), data.get('password'), data.get('role')
    db = get_db()
    if role:
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ? AND role = ?',
                          (email, hash_password(password), role)).fetchone()
    else:
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                          (email, hash_password(password))).fetchone()
    if not user:
        return jsonify({'message': 'Invalid email, password or role'}), 401
    token = secrets.token_hex(32)
    db.execute('UPDATE users SET token = ? WHERE id = ?', (token, user['id']))
    db.commit()
    log_event('INFO', f'User logged in: {email} (role: {user["role"]})')
    return jsonify({'token': token, 'name': user['name'], 'role': user['role'], 'user_id': user['id']}), 200
