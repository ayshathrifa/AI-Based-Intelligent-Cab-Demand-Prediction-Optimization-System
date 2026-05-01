import sys, os

# Always resolve paths relative to this file's location
THIS_FILE = os.path.abspath(__file__)
BACKEND_DIR  = os.path.dirname(THIS_FILE)
PROJECT_DIR  = os.path.dirname(BACKEND_DIR)
FRONTEND_DIR = os.path.join(PROJECT_DIR, 'frontend')
PAGES_DIR    = os.path.join(FRONTEND_DIR, 'pages')
CSS_DIR      = os.path.join(FRONTEND_DIR, 'css')
JS_DIR       = os.path.join(FRONTEND_DIR, 'js')

sys.path.insert(0, BACKEND_DIR)

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from database.db import init_db

from routes.auth import auth_bp
from routes.prediction import prediction_bp
from routes.realtime import realtime_bp
from routes.zones import zones_bp
from routes.driver import driver_bp
from routes.upload import upload_bp
from routes.train import train_bp
from routes.insights import insights_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

with app.app_context():
    init_db()

app.register_blueprint(auth_bp,       url_prefix='/api/auth')
app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
app.register_blueprint(realtime_bp,   url_prefix='/api/realtime')
app.register_blueprint(zones_bp,      url_prefix='/api/zones')
app.register_blueprint(driver_bp,     url_prefix='/api/driver')
app.register_blueprint(upload_bp,     url_prefix='/api/upload')
app.register_blueprint(train_bp,      url_prefix='/api/train')
app.register_blueprint(insights_bp,   url_prefix='/api/insights')
app.register_blueprint(admin_bp,      url_prefix='/api/admin')

@app.route('/debug')
def debug():
    return jsonify({
        'backend_dir':    BACKEND_DIR,
        'project_dir':    PROJECT_DIR,
        'frontend_dir':   FRONTEND_DIR,
        'pages_exists':   os.path.exists(PAGES_DIR),
        'index_exists':   os.path.exists(os.path.join(PAGES_DIR, 'index.html')),
        'cwd':            os.getcwd(),
        'pages_files':    os.listdir(PAGES_DIR) if os.path.exists(PAGES_DIR) else []
    })

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

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
