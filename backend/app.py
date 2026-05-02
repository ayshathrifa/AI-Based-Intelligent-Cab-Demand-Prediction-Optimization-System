import sys
import os
from flask import request

# ── Dynamic Path Resolution (Works on Render & Local) ─────────────────────────
BACKEND_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, 'frontend')
PAGES_DIR    = os.path.join(FRONTEND_DIR, 'pages')
CSS_DIR      = os.path.join(FRONTEND_DIR, 'css')
JS_DIR       = os.path.join(FRONTEND_DIR, 'js')

# Ensure backend modules can be found
sys.path.insert(0, BACKEND_DIR)

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

# ── App Initialization ────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=None, template_folder=None)

# Enable CORS for all routes (crucial for frontend connection)
CORS(app, resources={r"/*": {"origins": "*"}})

# ── Safe Database Initialization ──────────────────────────────────────────────
try:
    from config import Config
    app.config.from_object(Config)
except ImportError:
    print("⚠️ Warning: config.py not found. Using default configuration.")

try:
    from database.db import init_db
    with app.app_context():
        init_db()
except ImportError:
    print("⚠️ Warning: database/db.py not found. Skipping database initialization.")

# ── Safe Blueprint Registration ───────────────────────────────────────────────
blueprints = [
    ('routes.auth', 'auth_bp', '/api/auth'),
    ('routes.prediction', 'prediction_bp', '/api/prediction'),
    ('routes.realtime', 'realtime_bp', '/api/realtime'),
    ('routes.zones', 'zones_bp', '/api/zones'),
    ('routes.driver', 'driver_bp', '/api/driver'),
    ('routes.upload', 'upload_bp', '/api/upload'),
    ('routes.train', 'train_bp', '/api/train'),
    ('routes.insights', 'insights_bp', '/api/insights'),
    ('routes.admin', 'admin_bp', '/api/admin'),
]

for module_name, bp_name, url_prefix in blueprints:
    try:
        module = __import__(module_name, fromlist=[bp_name])
        blueprint = getattr(module, bp_name)
        app.register_blueprint(blueprint, url_prefix=url_prefix)
    except ImportError as e:
        print(f"⚠️ Warning: Could not import {module_name}. Skipping. Error: {e}")
    except Exception as e:
        print(f"⚠️ Warning: Error registering {module_name}. Error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# FRONTEND STATIC FILE ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return send_from_directory(PAGES_DIR, 'index.html')

@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory(PAGES_DIR, filename)

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory(CSS_DIR, filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory(JS_DIR, filename)

# Catch-all for frontend SPA routing (React, Vue, etc.)
@app.route('/<path:path>')
def catch_all(path):
    # If the user requests a specific file that exists, serve it. 
    # Otherwise, serve index.html so the frontend JS can handle the route.
    file_path = os.path.join(PAGES_DIR, path)
    if os.path.isfile(file_path):
        return send_from_directory(PAGES_DIR, path)
    return send_from_directory(PAGES_DIR, 'index.html')


# ═══════════════════════════════════════════════════════════════════════════════
# DEBUGGING ROUTE
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/debug')
def debug():
    return jsonify({
        'backend_dir':  BACKEND_DIR,
        'project_dir':  PROJECT_DIR,
        'frontend_dir': FRONTEND_DIR,
        'pages_exists': os.path.exists(PAGES_DIR),
        'index_exists': os.path.exists(os.path.join(PAGES_DIR, 'index.html')),
        'cwd':          os.getcwd(),
        'pages_files':  os.listdir(PAGES_DIR) if os.path.exists(PAGES_DIR) else []
    })


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    # Prevent infinite loops by checking if it's an API call
    if request.path.startswith('/api/'):
        return jsonify({"error": "API endpoint not found"}), 404
    return send_from_directory(PAGES_DIR, 'index.html')

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ═══════════════════════════════════════════════════════════════════════════════
# START SERVER
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Ensure directories exist for local testing
    os.makedirs(PAGES_DIR, exist_ok=True)
    os.makedirs(CSS_DIR, exist_ok=True)
    os.makedirs(JS_DIR, exist_ok=True)
    
    # Use production server settings (disable debug, bind to 0.0.0.0)
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))