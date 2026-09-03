from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

# ── DUAL ROUTING FORMSPREE ENDPOINTS ──
# Replace these strings with your actual Formspree IDs later
STANDARD_FORMSPREE_URL = "https://formspree.io"
CRISIS_FORMSPREE_URL   = "https://formspree.io"

# ── WEIGHTED SEVERITY DICTIONARY (Vercel Free-Tier Friendly) ──
CRISIS_WEIGHTS = {
    "suicide": 0.95, "suicidal": 0.95, "kill myself": 0.98, "end my life": 0.98, 
    "hang myself": 0.95, "slit my": 0.90, "cut myself": 0.85, "overdose": 0.85, 
    "want to die": 0.98, "goodbye world": 0.90, "hurt myself": 0.85, "self harm": 0.90
}

def analyze_crisis_score(text):
    text_clean = re.sub(r'[^\w\s]', '', text.lower())
    highest_score = 0.0
    matched_count = 0
    
    for phrase, weight in CRISIS_WEIGHTS.items():
        if phrase in text_clean:
            matched_count += 1
            if weight > highest_score:
                highest_score = weight
                
    if matched_count == 0:
        return 0.0
        
    # Bayesian multiplier: increase confidence if multiple keywords are grouped together
    context_multiplier = 1.0 + (min(matched_count - 1, 3) * 0.05)
    return min(highest_score * context_multiplier, 0.99)

@app.route('/api/submit-report', methods=['POST'])
def process_report():
    data = request.json or {}
    text_content = data.get('message', '').strip()
    provided_email = data.get('student_email', '').strip()
    category = data.get('category', 'General')
    severity = data.get('severity', 1)
    status = data.get('identity_status', 'STRICTLY_ANONYMOUS')
    escrow_token = data.get('device_escrow_token', 'NONE')

    if not text_content:
        return jsonify({"error": "Content field cannot be empty"}), 400

    # Execute text scanning
    ai_confidence = analyze_crisis_score(text_content)
    is_crisis_detected = ai_confidence >= 0.85 

    payload = {
        "category": category,
        "severity": severity,
        "message": text_content,
        "ai_score_confidence": f"{round(ai_confidence * 100, 2)}%",
        "identity_status": status
    }

    # ── BRANCH A: EMERGENCY INTERCEPT (THE 0.1%) ──
    if is_crisis_detected:
        payload["identity_status"] = "ANONYMOUS_CRISIS_TRIGGERED"
        payload["device_escrow_token"] = escrow_token  # Logs the hidden device token for school intervention
        payload["CRITICAL_ALERT"] = "🚨 IMMEDIATE COUNSELOR DISPATCH REQUIRED"
        
        try:
            requests.post(CRISIS_FORMSPREE_URL, json=payload, timeout=5)
        except Exception:
            pass
        return jsonify({"status": "crisis_intercepted", "trigger_ui_modal": True})

    # ── BRANCH B: GENERAL SECURE PROCESSING (THE 99.9%) ──
    else:
        if provided_email:
            payload["identity_status"] = "IDENTIFIED_BY_STUDENT"
            payload["student_email"] = provided_email

        try:
            requests.post(STANDARD_FORMSPREE_URL, json=payload, timeout=5)
        except Exception:
            pass
        return jsonify({"status": "success", "trigger_ui_modal": False})

if __name__ == '__main__':
    app.run()

