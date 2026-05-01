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

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
app.register_blueprint(realtime_bp, url_prefix='/api/realtime')
app.register_blueprint(zones_bp, url_prefix='/api/zones')
app.register_blueprint(driver_bp, url_prefix='/api/driver')
app.register_blueprint(upload_bp, url_prefix='/api/upload')
app.register_blueprint(train_bp, url_prefix='/api/train')
app.register_blueprint(insights_bp, url_prefix='/api/insights')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/')
def index():
    return send_from_directory('../frontend/pages', 'index.html')

@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory('../frontend/pages', filename)

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory('../frontend/css', filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory('../frontend/js', filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
