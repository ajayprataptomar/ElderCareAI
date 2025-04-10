# 👵🧠 ElderCareAI — Empowering Elderly Care with a Multi-Agent AI System

**ElderCareAI** is a modular, offline-capable multi-agent AI system designed to support elderly individuals living independently. It provides real-time health monitoring, fall detection, daily reminders, and AI-generated caregiver summaries. The solution is privacy-first, running entirely on local hardware with no internet dependency — ideal for edge devices or low-connectivity environments.

---

## 🧩 Features

- ✅ **Health Monitor Agent**
  - Monitors vitals: Heart Rate, Blood Pressure, Glucose, SpO₂
  - Detects abnormalities using a trained ML model
- ✅ **Safety Monitor Agent**
  - Detects fall risk from simulated sensor data
  - Uses an ML model trained on safety event datasets
- ✅ **Reminder Agent**
  - Sends voice/text reminders for medication & appointments
- ✅ **Communication Agent**
  - Generates natural language summaries using Ollama + LLaMA2
  - Designed for caregivers, family, and healthcare providers

---

## 💡 Problem Statement

> As part of the hackathon challenge to build an AI-powered multi-agent system for elderly care, the goal was to develop a collaborative solution that detects health anomalies, fall risks, and helps elderly users manage their daily activities — all while keeping caregivers informed.

---

## 🛠 Tech Stack

- 🐍 Python 3.9+
- 🎯 scikit-learn, pandas, joblib (ML)
- 🗣️ pyttsx3 (text-to-speech, optional)
- 🧠 [Ollama](https://ollama.com) + LLaMA2 (local LLM for summaries)
- 💽 SQLite (for storing reminders)
- 🍏 Metal GPU acceleration (Apple M2)

---

## 🧠 Architecture

```bash
📦 ElderCareAI/
├── agents/
│   ├── health_monitor.py       # ML-based vitals analysis
│   ├── safety_agent.py         # Fall detection model
│   ├── reminder_agent.py       # Static/dynamic reminder system
│   └── comms_agent.py          # Runs Ollama summary
├── models/
│   ├── health_model.pkl        # Trained health ML model
│   ├── fall_model.pkl          # Trained fall detection model
│   ├── fall_movement_encoder.pkl
│   └── fall_impact_encoder.pkl
├── Dataset/
│   ├── health_monitoring.csv
│   ├── safety_monitoring.csv
│   └── daily_reminder.csv
├── db/
│   └── reminders.db
├── main.py                    # Main File
├── gui.py                     # file for Graphical reperesntaion for mac, windows and other devices            
├── README.md
└── requirements.txt
