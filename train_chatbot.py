import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# ---------- Training data: (question examples, intent label) ----------
training_data = [
    # DoS
    ("what is dos attack", "dos"),
    ("explain dos", "dos"),
    ("denial of service", "dos"),
    ("how to prevent dos", "dos"),
    ("how to solve dos attack", "dos"),
    ("tell me about flooding attack", "dos"),

    # Probe
    ("what is probe attack", "probe"),
    ("explain probe", "probe"),
    ("what is scanning attack", "probe"),
    ("how to prevent probe attack", "probe"),
    ("reconnaissance attack meaning", "probe"),

    # R2L
    ("what is r2l attack", "r2l"),
    ("explain r2l", "r2l"),
    ("remote to local attack", "r2l"),
    ("how to prevent r2l", "r2l"),
    ("unauthorized remote access", "r2l"),

    # U2R
    ("what is u2r attack", "u2r"),
    ("explain u2r", "u2r"),
    ("user to root attack", "u2r"),
    ("how to prevent u2r", "u2r"),
    ("privilege escalation attack", "u2r"),

    # Normal
    ("what is normal traffic", "normal"),
    ("explain normal", "normal"),

    # Project explanation
    ("how does this project work", "project_info"),
    ("explain the project", "project_info"),
    ("what does this app do", "project_info"),
    ("how does the system work", "project_info"),
    ("what is this project about", "project_info"),

    # Model
    ("what ai model is used", "model_info"),
    ("which algorithm is used", "model_info"),
    ("what machine learning model", "model_info"),
    ("tell me about the model", "model_info"),

    # Accuracy
    ("what is the accuracy", "accuracy"),
    ("how accurate is the model", "accuracy"),

    # Dataset
    ("what dataset is used", "dataset"),
    ("tell me about the dataset", "dataset"),
    ("where does the data come from", "dataset"),

    # How to use
    ("how do i upload a file", "how_to_use"),
    ("how to use this app", "how_to_use"),
    ("how to analyze traffic", "how_to_use"),
    ("how to detect attacks", "how_to_use"),

    # History
    ("where can i see past scans", "history"),
    ("show scan history", "history"),

    # Analysis
    ("what does the analysis page show", "analysis"),
    ("explain attack analysis page", "analysis"),

    # About
    ("what is the about page", "about"),
    ("show model info page", "about"),

    # Greeting
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey there", "greeting"),
]

questions = [q for q, label in training_data]
labels = [label for q, label in training_data]

# ---------- Train the model ----------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

model = LogisticRegression()
model.fit(X, labels)

# ---------- Save model + vectorizer ----------
joblib.dump(model, "chatbot_model.pkl")
joblib.dump(vectorizer, "chatbot_vectorizer.pkl")

print("✅ Chatbot AI model trained and saved successfully!")