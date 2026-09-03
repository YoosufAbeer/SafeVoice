from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import os

app = Flask(__name__)
CORS(app)

# Disable background logging to maximize student data privacy
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Formspree endpoint hashes (swap these with your production keys later)
STANDARD_FORMSPREE_URL = "https://formspree.io"
CRISIS_FORMSPREE_URL   = "https://formspree.io"

@app.route('/api/submit-report', methods=['POST'])
def handle_submission():
    data = request.json or {}
    text_content = data.get('message', '').strip()
    provided_email = data.get('student_email', '').strip()
    category = data.get('category', 'General')
    severity = data.get('severity', 1)
    status = data.get('identity_status', 'STRICTLY_ANONYMOUS')
    escrow_token = data.get('device_escrow_token', 'NONE')

    if not text_content:
        return jsonify({"error": "Content cannot be empty"}), 400

    # Temporary validation keyword filter
    critical_words = ['suicide', 'self harm', 'end my life', 'kill myself', 'cut myself', 'goodbye']
    text_lower = text_content.lower()
    is_crisis = any(word in text_lower for word in critical_words)

    payload = {
        "category": category,
        "severity": severity,
        "message": text_content,
        "identity_status": status
    }

    if is_crisis:
        payload["identity_status"] = "ANONYMOUS_CRISIS_TRIGGERED"
        payload["device_escrow_token"] = escrow_token
        try:
            requests.post(CRISIS_FORMSPREE_URL, json=payload, timeout=5)
        except Exception:
            pass
        return jsonify({"status": "crisis_intercepted", "trigger_ui_modal": True})

    else:
        if provided_email:
            payload["identity_status"] = "IDENTIFIED_BY_STUDENT"
            payload["student_email"] = provided_email
        try:
            requests.post(STANDARD_FORMSPREE_URL, json=payload, timeout=5)
        except Exception:
            pass
        return jsonify({"status": "success", "trigger_ui_modal": False})
        
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "SafeVoice Python Backend is running smoothly!"
    }), 200

if __name__ == '__main__':
    # Grab the dynamic port Render allocates automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
