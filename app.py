from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
from chatbot import get_chatbot_response
from flask import jsonify
from database import init_db, save_scan, get_dashboard_stats, get_recent_scans, get_all_scans

app = Flask(__name__)

# ---------- Initialize database ----------
init_db()

# ---------- Store last detection results in memory ----------
last_results = {
    "results": None,
    "total": 0,
    "safe": 0,
    "malicious": 0,
    "attack_labels": [],
    "attack_values": [],
    "filename": None
}

# ---------- Load trained model and preprocessing objects ----------
model = joblib.load("model/saved_model.pkl")
scaler = joblib.load("model/scaler.pkl")
label_encoders = joblib.load("model/label_encoders.pkl")
target_encoder = joblib.load("model/target_encoder.pkl")
feature_columns = joblib.load("model/feature_columns.pkl")

input_columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"
]

# ---------- Route 1: Dashboard (home page) ----------
@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    recent = get_recent_scans()
    return render_template("dashboard.html", stats=stats, recent=recent, active="dashboard")

# ---------- Route 2: Threat Detection (upload + predict) ----------
@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "GET":
        return render_template(
            "detect.html",
            results=last_results["results"],
            total=last_results["total"],
            safe=last_results["safe"],
            malicious=last_results["malicious"],
            attack_labels=last_results["attack_labels"],
            attack_values=last_results["attack_values"],
            filename=last_results["filename"],
            active="detect"
        )

    # ---- POST: a new file was uploaded ----
    file = request.files["file"]
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    # Detect file type and read accordingly
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(filepath, header=None, names=input_columns, engine='openpyxl')
    elif file.filename.endswith('.xls'):
        df = pd.read_excel(filepath, header=None, names=input_columns, engine='xlrd')
    else:
        df = pd.read_csv(filepath, names=input_columns)

    for col in ["protocol_type", "service", "flag"]:
        le = label_encoders[col]
        df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        df[col] = le.transform(df[col])

    df = df[feature_columns]
    X_scaled = scaler.transform(df)

    predictions = model.predict(X_scaled)
    probabilities = model.predict_proba(X_scaled)

    results = []
    for i in range(len(predictions)):
        label = target_encoder.inverse_transform([predictions[i]])[0]
        confidence = round(max(probabilities[i]) * 100, 2)
        results.append({"row": i + 1, "prediction": label, "confidence": confidence})

    total = len(results)
    safe = sum(1 for r in results if r["prediction"] == "Normal")
    malicious = total - safe

    attack_counts = {"Normal": 0, "DoS": 0, "Probe": 0, "R2L": 0, "U2R": 0}
    for r in results:
        if r["prediction"] in attack_counts:
            attack_counts[r["prediction"]] += 1

   # Save this scan to the database
    save_scan(file.filename, total, safe, malicious, attack_counts)

    # Remember this as the last result (persists across page visits)
    last_results["results"] = results
    last_results["total"] = total
    last_results["safe"] = safe
    last_results["malicious"] = malicious
    last_results["attack_labels"] = list(attack_counts.keys())
    last_results["attack_values"] = list(attack_counts.values())
    last_results["filename"] = file.filename

    return render_template(
        "detect.html",
        results=results,
        total=total,
        safe=safe,
        malicious=malicious,
        attack_labels=list(attack_counts.keys()),
        attack_values=list(attack_counts.values()),
        filename=file.filename,
        active="detect"
    )

# ---------- Route 3: Attack Analysis ----------
@app.route("/analysis")
def analysis():
    attack_counts = dict(zip(last_results["attack_labels"], last_results["attack_values"]))
    stats = {
        "dos": attack_counts.get("DoS", 0),
        "probe": attack_counts.get("Probe", 0),
        "r2l": attack_counts.get("R2L", 0),
        "u2r": attack_counts.get("U2R", 0)
    }
    return render_template("analysis.html", stats=stats, active="analysis")

# ---------- Route 4: About / Model Info ----------
@app.route("/about")
def about():
    return render_template("about.html", active="about")

# ---------- Route 5: Scan History ----------
@app.route("/history")
def history():
    all_scans = get_all_scans()
    return render_template("history.html", all_scans=all_scans, active="history")

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        user_message = request.json.get("message", "")
        bot_reply = get_chatbot_response(user_message)
        return {"reply": bot_reply}
    return render_template("chatbot.html", active="chatbot")

if __name__ == "__main__":
    app.run(debug=True)

