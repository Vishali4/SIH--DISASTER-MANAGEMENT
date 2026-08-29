import os
import pandas as pd
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
FLOOD_MODEL_PATH = os.path.join(MODEL_DIR, "flood_model.joblib")
FIRE_MODEL_PATH = os.path.join(MODEL_DIR, "fire_model.joblib")

class EdgeAIInference:
    def __init__(self):
        # Try loading models
        try:
            self.flood_model = joblib.load(FLOOD_MODEL_PATH)
            print("Loaded Flood Edge-AI model successfully.")
        except Exception as e:
            print(f"Warning: Could not load flood model: {e}. Using rule fallback.")
            self.flood_model = None
            
        try:
            self.fire_model = joblib.load(FIRE_MODEL_PATH)
            print("Loaded Forest-Fire Edge-AI model successfully.")
        except Exception as e:
            print(f"Warning: Could not load fire model: {e}. Using rule fallback.")
            self.fire_model = None

    def evaluate_flood(self, temperature, humidity, water_distance, rain_value):
        """Runs inference for Flood sensor node (Node ID 1)."""
        # If model loaded, perform inference
        if self.flood_model:
            try:
                features = pd.DataFrame([{
                    'temperature': temperature,
                    'humidity': humidity,
                    'water_distance': water_distance,
                    'rain_value': rain_value
                }])
                risk = self.flood_model.predict(features)[0]
                
                # Get confidence score if tree supports probability
                probs = self.flood_model.predict_proba(features)[0]
                confidence = float(max(probs))
                return risk, confidence
            except Exception as e:
                print(f"Inference error on Flood Model: {e}. Falling back to rule-based.")
        
        # Rule-based fallback
        if water_distance <= 20.0 or (water_distance <= 35.0 and rain_value < 800):
            return "CRITICAL", 0.95
        elif water_distance <= 50.0 or (water_distance <= 75.0 and rain_value < 1500):
            return "HIGH", 0.85
        elif water_distance <= 95.0 or rain_value < 2000:
            return "WARNING", 0.70
        return "NORMAL", 0.99

    def evaluate_fire(self, temperature, humidity, smoke_value, flame_detected):
        """Runs inference for Forest-Fire sensor node (Node ID 2)."""
        if self.fire_model:
            try:
                features = pd.DataFrame([{
                    'temperature': temperature,
                    'humidity': humidity,
                    'smoke_value': smoke_value,
                    'flame_detected': int(flame_detected)
                }])
                risk = self.fire_model.predict(features)[0]
                
                probs = self.fire_model.predict_proba(features)[0]
                confidence = float(max(probs))
                return risk, confidence
            except Exception as e:
                print(f"Inference error on Fire Model: {e}. Falling back to rule-based.")
        
        # Rule-based fallback
        if flame_detected == 1 and smoke_value > 1500:
            return "CRITICAL", 0.98
        elif flame_detected == 1 or (smoke_value > 2000 and temperature > 40) or (smoke_value > 2500):
            return "HIGH", 0.88
        elif smoke_value > 800 or (temperature > 45 and humidity < 20):
            return "WARNING", 0.75
        return "NORMAL", 0.99

if __name__ == "__main__":
    ai = EdgeAIInference()
    
    # Test Flood Node
    print("\nTesting Flood Node Inference:")
    print("Normal Case:", ai.evaluate_flood(25.0, 60.0, 150.0, 4000))
    print("Critical Case:", ai.evaluate_flood(28.0, 95.0, 15.0, 200))
    
    # Test Fire Node
    print("\nTesting Fire Node Inference:")
    print("Normal Case:", ai.evaluate_fire(28.0, 45.0, 150, 0))
    print("Critical Case:", ai.evaluate_fire(42.0, 15.0, 2800, 1))
