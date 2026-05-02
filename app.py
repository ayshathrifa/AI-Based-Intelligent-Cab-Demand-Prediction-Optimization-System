import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, send_from_directory
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_DIR  = os.path.join(BASE_DIR, 'frontend', 'css')
JS_DIR   = os.path.join(BASE_DIR, 'frontend', 'js')

app = Flask(__name__, template_folder='frontend/templates')
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/realtime")
def realtime():
    return render_template("realtime.html")

@app.route("/zones")
def zones():
    return render_template("zones.html")

@app.route("/heatmap")
def heatmap():
    return render_template("heatmap.html")

@app.route("/driver")
def driver():
    return render_template("driver.html")

@app.route("/driver-dashboard")
def driver_dashboard():
    return render_template("driver-dashboard.html")

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/insights")
def insights():
    return render_template("insights.html")

@app.route("/train")
def train():
    return render_template("train.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/visualization")
def visualization():
    return render_template("visualization.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/peak")
def peak():
    return render_template("peak.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/pages/<path:filename>')
def pages(filename):
    return render_template(filename)

@app.route('/css/<path:filename>')
def css(filename):
    return send_from_directory(CSS_DIR, filename)

@app.route('/js/<path:filename>')
def js(filename):
    return send_from_directory(JS_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
