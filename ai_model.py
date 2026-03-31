import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

MODEL_PATH = "lap_predictor.pkl"

def train_model():

    df = pd.read_csv("data/training_data.csv")

    X = df[["avg_speed","max_speed","avg_throttle","avg_brake"]]
    y = df["lap_time"]

    model = RandomForestRegressor()

    model.fit(X,y)

    joblib.dump(model, MODEL_PATH)

    print("Model trained")

def load_model():
    return joblib.load(MODEL_PATH)

def extract_features(telemetry):

    features = {
        "avg_speed": telemetry["Speed"].mean(),
        "max_speed": telemetry["Speed"].max(),
        "avg_throttle": telemetry["Throttle"].mean(),
        "avg_brake": telemetry["Brake"].mean()
    }

    return pd.DataFrame([features])

def predict_lap_time(model, telemetry):

    features = extract_features(telemetry)

    prediction = model.predict(features)

    return prediction[0]