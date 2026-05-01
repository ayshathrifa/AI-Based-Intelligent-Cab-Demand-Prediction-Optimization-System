# 🚕 CabDemand AI — Cab Demand Prediction System

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?style=flat-square&logo=sqlite)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![HTML5](https://img.shields.io/badge/Frontend-HTML5%2FCSS3%2FJS-red?style=flat-square&logo=html5)

A full-stack machine learning web application that predicts cab demand across city zones using **Random Forest** and **Linear Regression**. Built with Flask, SQLite, and Vanilla JS with a dark-themed UI.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the backend
```bash
cd backend
python app.py
```

### 3. Open in browser
```
http://localhost:5000
```

---

## 📁 Project Structure

```
cab-demand-project/
├── frontend/
│   ├── pages/              # 19 HTML pages
│   ├── css/styles.css      # Dark theme stylesheet
│   └── js/                 # JavaScript modules
│       ├── auth.js         # Auth & role-based nav
│       ├── charts.js       # Dashboard charts
│       ├── driver.js       # Driver allocation logic
│       ├── heatmap.js      # Heatmap rendering
│       ├── main.js         # Dashboard data loader
│       └── prediction.js   # Prediction form handler
├── backend/
│   ├── app.py              # Flask entry point
│   ├── config.py           # App configuration
│   ├── routes/             # API blueprints
│   │   ├── admin.py        # Admin, logs, users, contact
│   │   ├── auth.py         # Signup, login, reset password
│   │   ├── driver.py       # Driver profiles, notifications
│   │   ├── insights.py     # AI insights
│   │   ├── prediction.py   # ML prediction & stats
│   │   ├── realtime.py     # Real-time prediction
│   │   ├── train.py        # Model training
│   │   ├── upload.py       # Dataset upload
│   │   └── zones.py        # Zone demand data
│   ├── models/
│   │   ├── predict_model.py
│   │   ├── train_model.py
│   │   └── compare_models.py
│   ├── services/
│   │   ├── demand_service.py
│   │   ├── optimization_service.py
│   │   └── weather_service.py
│   ├── utils/
│   │   ├── helpers.py
│   │   └── preprocessing.py
│   └── database/
│       ├── db.py           # DB init & helpers
│       └── db.sqlite3      # SQLite database
├── dataset/
│   ├── cab_data.csv
│   └── weather_data.csv
├── models/
│   ├── rf_model.pkl        # Trained Random Forest
│   └── lr_model.pkl        # Trained Linear Regression
└── requirements.txt
```

---

## 🌐 Pages

| Page | File | Role | Description |
|------|------|------|-------------|
| Home | `index.html` | All | Landing page |
| Login | `login.html` | All | Authentication with role selection |
| Signup | `signup.html` | All | User registration |
| Dashboard | `dashboard.html` | User / Admin | Demand overview & charts |
| Prediction | `prediction.html` | User / Admin | ML prediction form |
| Real-Time | `realtime.html` | User / Admin | Auto-detect time prediction |
| Zones | `zones.html` | User / Admin | Zone-wise demand analysis |
| Heatmap | `heatmap.html` | User / Admin | Visual demand intensity map |
| Driver Allocation | `driver.html` | User / Admin | AI driver deployment suggestions |
| Peak Hours | `peak.html` | User / Admin | Morning & evening peak analysis |
| Insights | `insights.html` | User / Admin | AI-powered demand insights |
| Visualization | `visualization.html` | User / Admin | Interactive charts |
| Admin Panel | `admin.html` | Admin only | System management |
| Upload Dataset | `upload.html` | Admin only | CSV dataset upload |
| Train Model | `train.html` | Admin only | Retrain ML models |
| Compare Models | `compare.html` | Admin only | RF vs Linear Regression |
| Driver Dashboard | `driver-dashboard.html` | Driver only | Personal zone & notifications |
| About | `about.html` | All | Project info & tech stack |
| Contact | `contact.html` | All | Contact form |

---

## 👥 User Roles

| Role | Access | Redirect After Login |
|------|--------|----------------------|
| **User** | Dashboard, Prediction, Zones, Heatmap, Drivers, Peak, Insights, Visualization, About, Contact | `dashboard.html` |
| **Admin** | Admin panel, Upload, Train, Compare Models, User Management, System Logs, Contact Inquiries | `admin.html` |
| **Driver** | Personal dashboard only — zone info, status update, notifications | `driver-dashboard.html` |

---

## 🤖 ML Models

| Model | Accuracy | R² Score | MAE |
|-------|----------|----------|-----|
| Random Forest | 94.2% | 0.91 | 3.8 |
| Linear Regression | 81.5% | 0.78 | 7.2 |

### Features used for prediction
- Hour of day
- Day of week
- Zone / Location
- Weather condition
- Temperature (°C)

---

## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/login` | Login — returns token, role, user_id |
| POST | `/api/auth/check-email` | Check if email exists |
| POST | `/api/auth/reset-password` | Reset password |

### Prediction
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/prediction/predict` | Predict cab demand |
| GET | `/api/prediction/stats` | Dashboard statistics |

### Driver
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/driver/allocate` | AI allocation suggestions |
| GET | `/api/driver/list` | All registered drivers |
| GET | `/api/driver/profile/<id>` | Driver profile + zone demand |
| PUT | `/api/driver/profile/<id>/status` | Update driver status |
| POST | `/api/driver/notify` | Send notification to a driver |
| POST | `/api/driver/notify-all` | Bulk notify all drivers |
| GET | `/api/driver/notifications/<id>` | Get driver notifications |
| PUT | `/api/driver/notifications/<id>/read` | Mark all notifications as read |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/logs` | System activity logs |
| GET | `/api/admin/users` | All registered users |
| PUT | `/api/admin/users/<id>` | Update user role |
| POST | `/api/admin/contact` | Submit contact message |
| GET | `/api/admin/contact` | View all contact inquiries |

### Other
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/zones/` | Zone-wise demand data |
| POST | `/api/upload` | Upload CSV dataset |
| POST | `/api/train` | Train ML model |
| GET | `/api/insights/` | AI insights |

---

## 🗄️ Database Schema

```sql
users           -- id, name, email, password, role, token, created_at
predictions     -- id, hour, day, zone, weather, temperature, predicted_demand, model_used, created_at
drivers         -- id, user_id, zone, status, rides_today
notifications   -- id, user_id, message, is_read, created_at
logs            -- id, level, message, created_at
contact_messages -- id, name, email, subject, message, created_at
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, Flask, Flask-CORS |
| Database | SQLite |
| ML | Scikit-learn (Random Forest, Linear Regression), Pandas, NumPy |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| Auth | SHA-256 password hashing, token-based sessions |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/cab-demand-project.git
cd cab-demand-project

# Install Python dependencies
pip install -r requirements.txt

# Start the server
cd backend
python app.py
```

The app will be available at **http://localhost:5000**

---

## 🧪 Sample API Calls

### Predict demand
```bash
curl -X POST http://localhost:5000/api/prediction/predict \
  -H "Content-Type: application/json" \
  -d '{"hour": 18, "day": 4, "zone": "downtown", "weather": "rain", "temperature": 22}'
```

### Train a model
```bash
curl -X POST http://localhost:5000/api/train \
  -H "Content-Type: application/json" \
  -d '{"model": "rf", "dataset": "cab_data.csv"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "yourpassword", "role": "admin"}'
```

---

## ✨ Features

- 🔮 **ML Demand Prediction** — Random Forest & Linear Regression models
- ⚡ **Real-Time Prediction** — Auto-detects current time and location
- 🗺️ **Zone Analysis** — Demand breakdown across 8 city zones
- 🔥 **Demand Heatmap** — Visual intensity grid by hour and zone
- 🚗 **Driver Management** — AI allocation suggestions with real notifications
- 📊 **Data Visualization** — Bar, line, area, pie, radar charts
- 🧠 **AI Insights** — Weather, time, and event-based demand patterns
- ⚙️ **Admin Panel** — User management, system logs, contact inquiries
- 📤 **Dataset Upload** — Upload new CSV data for retraining
- 🔔 **Driver Notifications** — Real-time zone assignment alerts
- 🔐 **Role-Based Access** — User, Admin, Driver with separate dashboards
- 📬 **Contact System** — Messages saved to DB and visible in admin panel

---

## 📄 License

This project is built for educational and portfolio purposes.
