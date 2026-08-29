import os
import sys
from flask import Flask, render_template, jsonify

# Add parent directory to path to import database modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

app = Flask(__name__)

# Ensure DB is initialized
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Returns the latest sensor logs and current risk status."""
    latest = database.get_latest_readings(limit=15)
    
    # Extract latest readings for node 1 & 2
    node1_data = database.get_recent_node_readings(node_id=1, limit=1)
    node2_data = database.get_recent_node_readings(node_id=2, limit=1)
    
    status = {
        "node1": node1_data[0] if node1_data else None,
        "node2": node2_data[0] if node2_data else None,
        "logs": latest
    }
    return jsonify(status)

@app.route('/api/history')
def get_history():
    """Returns past 100 logs for charting."""
    logs = database.get_latest_readings(limit=100)
    # Reverse to make chronological for charting
    logs.reverse()
    return jsonify(logs)

if __name__ == '__main__':
    print("Starting Web Dashboard on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
