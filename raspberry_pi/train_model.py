import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Make directory for model saving if it doesn't exist
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
os.makedirs(MODEL_DIR, exist_ok=True)

def generate_flood_dataset(n_samples=2000):
    """Generates synthetic dataset for flood monitoring."""
    np.random.seed(42)
    
    # Generate random features
    temperature = np.random.uniform(15, 45, n_samples)
    humidity = np.random.uniform(30, 95, n_samples)
    
    # Water distance: 10cm to 200cm. (Smaller means higher water level!)
    water_distance = np.random.uniform(5, 200, n_samples)
    
    # Rain value: 0 to 4095 (analog). Standard sensor: 4095 is dry, 0 is fully wet.
    rain_value = np.random.uniform(0, 4095, n_samples)
    
    data = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'water_distance': water_distance,
        'rain_value': rain_value
    })
    
    # Label logic:
    # Water level is very high if distance <= 30cm
    # High if distance <= 60cm
    # Warning if distance <= 100cm
    # Wet if rain_value < 1500 (moderate rain) or < 500 (heavy rain)
    risk_levels = []
    for index, row in data.iterrows():
        dist = row['water_distance']
        rain = row['rain_value']
        
        if dist <= 20 or (dist <= 35 and rain < 800):
            risk_levels.append("CRITICAL")
        elif dist <= 50 or (dist <= 75 and rain < 1500):
            risk_levels.append("HIGH")
        elif dist <= 95 or rain < 2000:
            risk_levels.append("WARNING")
        else:
            risk_levels.append("NORMAL")
            
    data['risk_level'] = risk_levels
    return data

def generate_fire_dataset(n_samples=2000):
    """Generates synthetic dataset for forest fire monitoring."""
    np.random.seed(43)
    
    # Generate random features
    temperature = np.random.uniform(20, 55, n_samples)
    humidity = np.random.uniform(10, 80, n_samples)
    
    # Smoke value (MQ-2 analog): 100 (clean air) to 4000 (dense smoke)
    smoke_value = np.random.uniform(100, 4095, n_samples)
    
    # Flame sensor: 0 = No flame, 1 = Flame detected
    flame_detected = np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])
    
    data = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'smoke_value': smoke_value,
        'flame_detected': flame_detected
    })
    
    # Label logic:
    # High temperature, low humidity, smoke, flame detection
    risk_levels = []
    for index, row in data.iterrows():
        temp = row['temperature']
        hum = row['humidity']
        smoke = row['smoke_value']
        flame = row['flame_detected']
        
        if flame == 1 and smoke > 1500:
            risk_levels.append("CRITICAL")
        elif flame == 1 or (smoke > 2000 and temp > 40) or (smoke > 2500):
            risk_levels.append("HIGH")
        elif smoke > 800 or (temp > 45 and hum < 20):
            risk_levels.append("WARNING")
        else:
            risk_levels.append("NORMAL")
            
    data['risk_level'] = risk_levels
    return data

def train_and_save_models():
    print("Generating training data...")
    flood_df = generate_flood_dataset()
    fire_df = generate_fire_dataset()
    
    # 1. Flood Node Model
    print("Training Flood Risk Classification Model...")
    X_flood = flood_df[['temperature', 'humidity', 'water_distance', 'rain_value']]
    y_flood = flood_df['risk_level']
    
    flood_model = DecisionTreeClassifier(max_depth=5, random_state=42)
    flood_model.fit(X_flood, y_flood)
    
    flood_path = os.path.join(MODEL_DIR, "flood_model.joblib")
    joblib.dump(flood_model, flood_path)
    print(f"Flood model saved to {flood_path}")
    
    # 2. Fire Node Model
    print("Training Forest-Fire Risk Classification Model...")
    X_fire = fire_df[['temperature', 'humidity', 'smoke_value', 'flame_detected']]
    y_fire = fire_df['risk_level']
    
    fire_model = DecisionTreeClassifier(max_depth=5, random_state=42)
    fire_model.fit(X_fire, y_fire)
    
    fire_path = os.path.join(MODEL_DIR, "fire_model.joblib")
    joblib.dump(fire_model, fire_path)
    print(f"Fire model saved to {fire_path}")
    
if __name__ == "__main__":
    train_and_save_models()
