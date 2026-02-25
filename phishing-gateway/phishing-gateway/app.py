from flask import Flask, render_template, request, redirect, url_for
import os
import joblib
import json
import time
from models.database import db, PhishingLog
from models.rule_engine import run_rule_checks
from models.feature_extractor import preprocess_text

app = Flask(__name__)

# region agent log
def _agent_log(run_id, hypothesis_id, location, message, data=None):
    try:
        log_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "debug-5e11ae.log")
        entry = {
            "sessionId": "5e11ae",
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass
# endregion

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'gateway.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Load AI Assets
try:
    _agent_log("run1", "H2", "app.py:MODEL_LOAD_START", "Starting model and vectorizer load", {})
    MODEL = joblib.load(os.path.join(BASE_DIR, 'models', 'gateway_model.pkl'))
    VEC = joblib.load(os.path.join(BASE_DIR, 'models', 'vectorizer.pkl'))
    _agent_log("run1", "H2", "app.py:MODEL_LOAD_SUCCESS", "Model and vectorizer loaded", {})
except Exception as exc:
    _agent_log(
        "run1",
        "H2",
        "app.py:MODEL_LOAD_ERROR",
        "Error loading model/vectorizer",
        {"errorType": type(exc).__name__, "errorMessage": str(exc)},
    )
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    message = request.form.get('content', '')
    
    # Step 1: Rule Engine
    is_phishing, reason = run_rule_checks(message)
    
    # Step 2: AI Model (if rules pass)
    if not is_phishing:
        clean_text = preprocess_text(message)
        vectorized = VEC.transform([clean_text])
        prediction = MODEL.predict(vectorized)[0]
        if prediction == 1:
            is_phishing = True
            reason = "AI Prediction (Probable Spam)"
        else:
            reason = "Verified Safe"

    # Step 3: Persistence
    log = PhishingLog(content=message, is_phishing=is_phishing, reason=reason)
    db.session.add(log)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    logs = PhishingLog.query.order_by(PhishingLog.timestamp.desc()).all()
    return render_template('dashboard.html', logs=logs)

if __name__ == '__main__':
    try:
        _agent_log("run1", "H3", "app.py:MAIN_START", "Starting app main block", {})
        with app.app_context():
            _agent_log("run1", "H3", "app.py:DB_CREATE_START", "Creating all DB tables", {})
            db.create_all()
            _agent_log("run1", "H3", "app.py:DB_CREATE_SUCCESS", "DB tables created", {})
        _agent_log("run1", "H4", "app.py:FLASK_RUN_START", "Calling app.run()", {"debug": True})
        app.run(debug=True)
    except Exception as exc:
        _agent_log(
            "run1",
            "H1",
            "app.py:MAIN_EXCEPTION",
            "Unhandled exception in __main__",
            {"errorType": type(exc).__name__, "errorMessage": str(exc)},
        )
        raise