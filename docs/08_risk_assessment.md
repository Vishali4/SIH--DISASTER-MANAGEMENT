# 08 Risk Assessment Matrix

## 1. Alert Level Definition

The Environmental Intelligence Network outputs four alert classifications depending on sensor signals parsed by the local AI models.

| Risk Level | Target Indicator | Buzzer Behavior | LCD Backlight/Text | Action Required |
|---|---|---|---|---|
| **NORMAL** | Green LED ON | OFF | Static "System: OK" | Continuous surveillance; no threat detected. |
| **WARNING** | Yellow LED ON | Intermittent beep (1s interval) | "Alert: WARNING" | Monitor parameters closely. Alert field engineer. |
| **HIGH** | Red LED ON | Fast intermittent beep (0.2s interval) | "Alert: HIGH" | Evacuation prep recommended. Deploy response teams. |
| **CRITICAL** | Red LED ON | Continuous high-frequency siren | "Alert: CRITICAL" | Immediate evacuation. Emergency protocols active. |

---

## 2. Risk Heuristics (Rule-Based Fallback)

Should the AI model fail to load, the system triggers the following rules:

### Flood Evaluation (Node 1):
- **CRITICAL**: Water distance $\le$ 20cm OR (water distance $\le$ 35cm and rain analog value $<$ 800).
- **HIGH**: Water distance $\le$ 50cm OR (water distance $\le$ 75cm and rain analog value $<$ 1500).
- **WARNING**: Water distance $\le$ 95cm OR rain analog value $<$ 2000.
- **NORMAL**: Water distance $>$ 95cm and rain analog value $\ge$ 2000.

### Forest-Fire Evaluation (Node 2):
- **CRITICAL**: Flame detected AND smoke analog value $>$ 1500.
- **HIGH**: Flame detected OR (smoke value $>$ 2000 and temperature $>$ 40°C) OR smoke value $>$ 2500.
- **WARNING**: Smoke value $>$ 800 OR (temperature $>$ 45°C and humidity $<$ 20%).
- **NORMAL**: Otherwise.
