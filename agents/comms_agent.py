# agents/comms_agent.py

import subprocess
import json
from datetime import datetime

class CommunicationAgent:
    def __init__(self, model_name="llama2"):
        self.model = model_name  # ollama model must be downloaded locally

    def generate_response(self, prompt):
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )
            response = result.stdout.decode("utf-8").strip()
            return response
        except Exception as e:
            return f"Error running Ollama model: {str(e)}"

    def summarize_alerts(self, health_alerts, safety_alerts, reminders):
        prompt = "Summarize these alerts for caregiver:\n\n"

        if health_alerts:
            prompt += f"Health Alerts:\n{chr(10).join(health_alerts)}\n\n"
        if safety_alerts:
            prompt += f"Safety Alerts:\n{chr(10).join(safety_alerts)}\n\n"
        if reminders:
            reminder_msgs = [f"Reminder at {time}: {msg}" for msg, time in reminders]
            prompt += f"Reminders:\n{chr(10).join(reminder_msgs)}\n\n"

        prompt += "\nRespond with a short, calm summary in natural language."

        return self.generate_response(prompt)

    async def run(self):
        # placeholder if future real-time chat is needed
        pass
