import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
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

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR    = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'pages'))
CSS_DIR      = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'css'))
JS_DIR       = os.path.abspath(os.path.join(BASE_DIR, '..', 'frontend', 'js'))

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

@app.route("/")
def home():
    return "Backend is running"

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
