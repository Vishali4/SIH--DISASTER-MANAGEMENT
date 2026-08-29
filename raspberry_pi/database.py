import sqlite3
import os
import time

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "disaster_data.db")

def get_db_connection():
    """Establishes connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Sensor data table (stores reading history)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOCTINCR,
            node_id INTEGER NOT NULL,
            packet_id INTEGER,
            timestamp REAL NOT NULL,
            temperature REAL,
            humidity REAL,
            water_distance REAL,
            rain_value INTEGER,
            smoke_value INTEGER,
            flame_detected INTEGER,
            risk_level TEXT,
            confidence REAL
        )
    """)

    # Fix typo in table creation: AUTOINCREMENT (was AUTOCTINCR)
    # Let's write the correct query:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_logs_fixed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id INTEGER NOT NULL,
            packet_id INTEGER,
            timestamp REAL NOT NULL,
            temperature REAL,
            humidity REAL,
            water_distance REAL,
            rain_value INTEGER,
            smoke_value INTEGER,
            flame_detected INTEGER,
            risk_level TEXT,
            confidence REAL
        )
    """)
    # We drop the old one if it exists or just create the correct one:
    cursor.execute("DROP TABLE IF EXISTS sensor_logs")
    cursor.execute("ALTER TABLE sensor_logs_fixed RENAME TO sensor_logs")
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DATABASE_PATH}")

def log_sensor_data(node_id, packet_id, temperature, humidity, 
                    water_distance=None, rain_value=None, 
                    smoke_value=None, flame_detected=None, 
                    risk_level="NORMAL", confidence=1.0):
    """Logs a new sensor reading to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    timestamp = time.time()
    try:
        cursor.execute("""
            INSERT INTO sensor_logs (
                node_id, packet_id, timestamp, temperature, humidity, 
                water_distance, rain_value, smoke_value, flame_detected, 
                risk_level, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            node_id, packet_id, timestamp, temperature, humidity,
            water_distance, rain_value, smoke_value, flame_detected,
            risk_level, confidence
        ))
        conn.commit()
    except Exception as e:
        print(f"Error logging sensor data to DB: {e}")
    finally:
        conn.close()

def get_latest_readings(limit=100):
    """Retrieves the latest logs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM sensor_logs ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_recent_node_readings(node_id, limit=30):
    """Retrieves the latest logs for a specific node."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM sensor_logs WHERE node_id = ? ORDER BY id DESC LIMIT ?
    """, (node_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

if __name__ == "__main__":
    init_db()
