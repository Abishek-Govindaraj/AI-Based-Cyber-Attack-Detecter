import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
import os

# ---------- Step 1: Define column names (NSL-KDD has no header row) ----------
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes","land",
    "wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised",
    "root_shell","su_attempted","num_root","num_file_creations","num_shells",
    "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count",
    "srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
    "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
    "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate",
    "label","difficulty"
]

# ---------- Step 2: Load dataset ----------
print("Loading dataset...")
df = pd.read_csv("dataset/KDDTrain+.txt", names=columns)
print("Shape:", df.shape)
print(df["label"].value_counts().head(10))

# ---------- Step 3: Map attack labels into categories ----------
attack_map = {
    "normal": "Normal",
    "back": "DoS", "land": "DoS", "neptune": "DoS", "pod": "DoS",
    "smurf": "DoS", "teardrop": "DoS", "apache2": "DoS", "udpstorm": "DoS",
    "processtable": "DoS", "worm": "DoS", "mailbomb": "DoS",
    "ipsweep": "Probe", "nmap": "Probe", "portsweep": "Probe",
    "satan": "Probe", "mscan": "Probe", "saint": "Probe",
    "ftp_write": "R2L", "guess_passwd": "R2L", "imap": "R2L",
    "multihop": "R2L", "phf": "R2L", "spy": "R2L", "warezclient": "R2L",
    "warezmaster": "R2L", "sendmail": "R2L", "named": "R2L",
    "snmpgetattack": "R2L", "snmpguess": "R2L", "xlock": "R2L",
    "xsnoop": "R2L", "httptunnel": "R2L",
    "buffer_overflow": "U2R", "loadmodule": "U2R", "perl": "U2R",
    "rootkit": "U2R", "ps": "U2R", "sqlattack": "U2R", "xterm": "U2R"
}
df["attack_category"] = df["label"].map(attack_map)
df["attack_category"] = df["attack_category"].fillna("Unknown")
df = df[df["attack_category"] != "Unknown"]  # drop any unmapped labels

print("\nCategory distribution:")
print(df["attack_category"].value_counts())

# ---------- Step 4: Drop unneeded columns ----------
df = df.drop(["label", "difficulty"], axis=1)

# ---------- Step 5: Encode categorical columns ----------
categorical_cols = ["protocol_type", "service", "flag"]
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# ---------- Step 6: Encode target ----------
target_encoder = LabelEncoder()
df["attack_category"] = target_encoder.fit_transform(df["attack_category"])

# ---------- Step 7: Split features and target ----------
X = df.drop("attack_category", axis=1)
y = df["attack_category"]

feature_columns = X.columns.tolist()

# ---------- Step 8: Scale numeric features ----------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------- Step 9: Train/test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ---------- Step 10: Train Random Forest ----------
print("\nTraining Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# ---------- Step 11: Evaluate ----------
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

# ---------- Step 12: Save everything ----------
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/saved_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
joblib.dump(label_encoders, "model/label_encoders.pkl")
joblib.dump(target_encoder, "model/target_encoder.pkl")
joblib.dump(feature_columns, "model/feature_columns.pkl")

print("\n✅ Model and preprocessing objects saved in 'model/' folder.")