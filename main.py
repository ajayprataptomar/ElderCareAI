import asyncio
import pyttsx3  # 🔊 Text-to-speech engine

from agents.health_monitor import HealthMonitorAgent
from agents.safety_agent import SafetyAgent
from agents.reminder_agent import ReminderAgent
from agents.comms_agent import CommunicationAgent
from db.database import init_db

async def main():
    print(" Initializing Elderly Care Multi-Agent System...\n")
    init_db()

    # Initialize agents
    health_agent = HealthMonitorAgent()
    safety_agent = SafetyAgent()
    reminder_agent = ReminderAgent()
    comms_agent = CommunicationAgent()

    # Run each agent and collect their outputs
    print("Running health checks...")
    health_alerts = health_agent.run()

    print(" Running safety checks...")
    safety_alerts = safety_agent.run()

    print(" Fetching today's reminders...")
    reminders = reminder_agent.run()

    print("Generating summary using Ollama LLM...\n")
    summary = comms_agent.summarize_alerts(health_alerts, safety_alerts, reminders)

    # Output results
    print(" Summary for Caregiver:\n")
    print(summary)

    #  Speak the summary aloud
    engine = pyttsx3.init()
    engine.setProperty('rate', 165)  # Optional: adjust speaking rate
    engine.say(summary)
    engine.runAndWait()

    print("\n All systems checked.")

if __name__ == "__main__":
    asyncio.run(main())
