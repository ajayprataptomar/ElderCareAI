# db/database.py

import sqlite3
import os

DB_PATH = "eldercare.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Health logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                heart_rate INTEGER,
                blood_pressure_sys INTEGER,
                blood_pressure_dia INTEGER,
                glucose INTEGER
            )
        """)

        # Safety logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS safety_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_moving INTEGER,
                fall_detected INTEGER
            )
        """)

        # Reminders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                message TEXT
            )
        """)

        # Sample reminders
        cursor.execute("""
            INSERT INTO reminders (date, time, message)
            VALUES
                (DATE('now'), '09:00', 'Take your morning medication.'),
                (DATE('now'), '14:00', 'Doctor appointment at 2 PM.'),
                (DATE('now'), '20:00', 'Take your evening medication.')
        """)

        conn.commit()
        conn.close()
        print("✅ Database initialized successfully.")
    else:
        print("ℹ️ Database already exists.")

if __name__ == "__main__":
    init_db()
