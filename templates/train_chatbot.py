import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

training_data = [
    # DoS
    ("what is dos attack", "dos"),
    ("explain dos", "dos"),
    ("explain the dos attack", "dos"),
    ("denial of service", "dos"),
    ("how to prevent dos", "dos"),
    ("how to solve dos attack", "dos"),
    ("tell me about flooding attack", "dos"),
    ("what does dos mean", "dos"),
    ("dos attack meaning", "dos"),

    # Probe
    ("what is probe attack", "probe"),
    ("explain probe", "probe"),
    ("explain the probe attack", "probe"),
    ("what is scanning attack", "probe"),
    ("how to prevent probe attack", "probe"),
    ("reconnaissance attack meaning", "probe"),
    ("what does probe mean", "probe"),
    ("probe attack meaning", "probe"),

    # R2L
    ("what is r2l attack", "r2l"),
    ("explain r2l", "r2l"),
    ("explain about r2l", "r2l"),
    ("explain the r2l attack", "r2l"),
    ("remote to local attack", "r2l"),
    ("how to prevent r2l", "r2l"),
    ("unauthorized remote access", "r2l"),
    ("what does r2l mean", "r2l"),
    ("r2l attack meaning", "r2l"),
    ("tell me about r2l", "r2l"),

    # U2R
    ("what is u2r attack", "u2r"),
    ("explain u2r", "u2r"),
    ("explain about u2r", "u2r"),
    ("explain the u2r attack", "u2r"),
    ("user to root attack", "u2r"),
    ("how to prevent u2r", "u2r"),
    ("privilege escalation attack", "u2r"),
    ("what does u2r mean", "u2r"),
    ("u2r attack meaning", "u2r"),
    ("tell me about u2r", "u2r"),

    # Normal
    ("what is normal traffic", "normal"),
    ("explain normal", "normal"),
    ("explain about normal traffic", "normal"),
    ("what does normal mean", "normal"),

    # Project explanation
    ("how does this project work", "project_info"),
    ("explain the project", "project_info"),
    ("what does this app do", "project_info"),
    ("how does the system work", "project_info"),
    ("what is this project about", "project_info"),
    ("tell me about this project", "project_info"),
    ("what is cyberguard ai", "project_info"),

    # Model
    ("what ai model is used", "model_info"),
    ("which algorithm is used", "model_info"),
    ("what machine learning model", "model_info"),
    ("tell me about the model", "model_info"),
    ("which model is used", "model_info"),
    ("what algorithm classifies traffic", "model_info"),
    ("which ai is used", "model_info"),

    # Accuracy
    ("what is the accuracy", "accuracy"),
    ("how accurate is the model", "accuracy"),
    ("model accuracy", "accuracy"),

    # Dataset
    ("what dataset is used", "dataset"),
    ("tell me about the dataset", "dataset"),
    ("where does the data come from", "dataset"),
    ("what data was used to train", "dataset"),

    # How to use
    ("how do i upload a file", "how_to_use"),
    ("how to use this app", "how_to_use"),
    ("how to use the app", "how_to_use"),
    ("how to analyze traffic", "how_to_use"),
    ("how to detect attacks", "how_to_use"),
    ("how do i use this", "how_to_use"),
    ("how does the app work", "how_to_use"),
    ("how to upload a file", "how_to_use"),
    ("how to scan traffic", "how_to_use"),
    ("how do i check for attacks", "how_to_use"),
    ("steps to use the app", "how_to_use"),

    # History
    ("where can i see past scans", "history"),
    ("show scan history", "history"),
    ("where is scan history", "history"),
    ("view previous scans", "history"),

    # Analysis
    ("what does the analysis page show", "analysis"),
    ("explain attack analysis page", "analysis"),
    ("what is the analysis page", "analysis"),

    # About
    ("what is the about page", "about"),
    ("show model info page", "about"),
    ("where is the about page", "about"),

    # Greeting
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey there", "greeting"),
    ("hey", "greeting"),
]

questions = [q for q, label in training_data]
labels = [label for q, label in training_data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

joblib.dump(model, "chatbot_model.pkl")
joblib.dump(vectorizer, "chatbot_vectorizer.pkl")

print("✅ Chatbot AI model trained and saved successfully!")