import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cabdemand-secret-key-2024')
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database', 'db.sqlite3')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'dataset')
    MODEL_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'models')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'csv'}
    RF_MODEL_PATH = os.path.join(MODEL_FOLDER, 'rf_model.pkl')
    LR_MODEL_PATH = os.path.join(MODEL_FOLDER, 'lr_model.pkl')
