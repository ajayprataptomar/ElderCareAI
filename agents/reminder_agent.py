# agents/reminder_agent.py

import sqlite3
import datetime

DB_PATH = "db/eldercare.db"

class ReminderAgent:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def get_todays_reminders(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT message, time FROM reminders WHERE date = ?
        """, (today,))
        return self.cursor.fetchall()

    def send_reminders(self, reminders):
        for reminder in reminders:
            message, time = reminder
            print(f"[Reminder at {time}] {message}")  # Simulate voice note

    def run(self):
        reminders = self.get_todays_reminders()
        self.send_reminders(reminders)
        return reminders
