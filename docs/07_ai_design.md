# 07 Edge-AI Design

To execute intelligence locally on a Raspberry Pi without depending on cloud servers, the architecture utilizes a lightweight machine learning classification model trained using `scikit-learn`.

## 1. Machine Learning Model Selection
A **Decision Tree Classifier** was chosen for the initial prototype:
- **Low Footprint**: Consumes very little RAM/CPU, making it perfect for Raspberry Pi deployment.
- **Fast Inference**: Runs prediction functions in less than 1 millisecond.
- **Explainability**: Decision nodes can be easily audited, visualized, and exported to C/C++ or micro-controllers in the future if required.

## 2. Training Workflow
1. **Dataset Generation**: Synthetic datasets are created representing multiple hazard combinations (e.g. rising water levels + heavy rain, hot dry weather + sudden smoke spikes).
2. **Features**:
   - **Flood Node**: Temperature, Humidity, Water Distance, Rain Value.
   - **Fire Node**: Temperature, Humidity, Smoke Value, Flame Detected.
3. **Training Script**: Run [`train_model.py`](file:///C:/Users/VISHALI/.gemini/antigravity-ide/scratch/SIH-DISASTER-MANAGEMENT/raspberry_pi/train_model.py). The script generates datasets, fits decision trees, and exports the models to serialized files (`flood_model.joblib` and `fire_model.joblib`).

## 3. Inference Engine
The file [`edge_ai.py`](file:///C:/Users/VISHALI/.gemini/antigravity-ide/scratch/SIH-DISASTER-MANAGEMENT/raspberry_pi/edge_ai.py) loads these model files on startup.
- **Validation**: Incoming packets are vetted to match acceptable limits before running prediction.
- **Class Output**: Yields predicted hazard level (`NORMAL`, `WARNING`, `HIGH`, `CRITICAL`).
- **Confidence Output**: Utilizes the leaf-node probability distribution of the decision tree to provide a confidence percentage for each classification.
