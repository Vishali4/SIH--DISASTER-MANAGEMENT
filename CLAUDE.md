# CLAUDE.md

Developer guidelines, common commands, and execution workflows for the Environmental Intelligence Network.

## 🛠 Command Cheatsheet

### 1. Python Environment Setup
Use conda Python (version 3.13.9) to execute commands.
```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Model Training
Generate training data and serialize models (`flood_model.joblib` and `fire_model.joblib`):
```bash
C:\Users\VISHALI\anaconda3\python.exe raspberry_pi/train_model.py
```

### 3. Running Hub Orchestration
Start the central sensor reception loop (runs in simulation mode if serial LoRa receiver is absent):
```bash
C:\Users\VISHALI\anaconda3\python.exe raspberry_pi/main.py
```

### 4. Running Web Dashboard
Start the local dashboard server (accessible on `http://localhost:5000`):
```bash
C:\Users\VISHALI\anaconda3\python.exe raspberry_pi/dashboard/app.py
```

### 5. Run Verification Script
Validate AI model predictions and rules:
```bash
C:\Users\VISHALI\anaconda3\python.exe raspberry_pi/edge_ai.py
```

## 📐 Project Rules
- **No Internet Dependency**: Any code introduced to RPi modules must be capable of execution offline. Never import scripts or styling sheets using external CDN links in index pages unless a local fallback exists.
- **Hardware Simulation Fallbacks**: Always design peripheral scripts (LCD, Buzzer, LEDs, Serial LoRa) with automated mock check-blocks so developers can test systems on standard Windows/macOS/Linux environments.
