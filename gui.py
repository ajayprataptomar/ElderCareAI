import sys
import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QHBoxLayout, QGraphicsOpacityEffect, QFrame
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QTimer
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtChart import QChart, QChartView, QPieSeries

from agents.health_monitor import HealthMonitorAgent
from agents.safety_agent import SafetyAgent
from agents.reminder_agent import ReminderAgent


class FlipCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(220)
        self.setStyleSheet("background-color: transparent; border-radius: 20px;")

        self.gradient = QFrame(self)
        self.gradient.setGeometry(0, 0, self.width(), self.height() + 20)
        self.gradient.setStyleSheet("""
            QFrame {
                background: qconicalgradient(cx:0.5, cy:0.5, angle:0,
                    stop:0 #00b7ff, stop:1 #ff30ff);
                border-radius: 20px;
            }
        """)
        self.gradient.lower()

        self.inner = QLabel(self)
        self.inner.setWordWrap(True)
        self.inner.setAlignment(Qt.AlignTop)
        self.inner.setGeometry(5, 5, self.width() - 10, self.height() - 10)
        self.inner.setStyleSheet("""
            QLabel {
                background-color: #07182E;
                border-radius: 15px;
                padding: 16px;
                font-size: 16px;
                font-family: 'Poppins';
                color: white;
            }
        """)
        self.inner.raise_()

        self.opacity_effect = QGraphicsOpacityEffect(self.inner)
        self.inner.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)

        self.rotation_angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_gradient)
        self.timer.start(30)

    def update_content(self, text):
        self.inner.setText(text)
        self.fade_anim.start()

    def rotate_gradient(self):
        self.rotation_angle = (self.rotation_angle + 1) % 360
        self.gradient.setStyleSheet(f"""
            QFrame {{
                background: qconicalgradient(cx:0.5, cy:0.5, angle:{self.rotation_angle},
                    stop:0 #00b7ff, stop:1 #ff30ff);
                border-radius: 20px;
            }}
        """)


class ReminderBox(QLabel):
    def __init__(self):
        super().__init__()
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignTop)
        self.setStyleSheet("""
            QLabel {
                background-color: #1a1a2e;
                border: 2px solid #00b7ff;
                border-radius: 16px;
                font-size: 15px;
                color: #ffffff;
                padding: 16px;
                font-family: 'Poppins';
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_reminder_time)
        self.timer.start(1000)
        self.reminders = []
        self.agent = ReminderAgent()

    def update_reminder_time(self):
        now = datetime.datetime.now()
        self.reminders = self.agent.get_todays_reminders()
        display = "<b>⏳ Today's Reminders:</b><br>"

        if not self.reminders:
            display += "No reminders set for today."
        else:
            for r in self.reminders:
                rem_time = datetime.datetime.strptime(r["time"], "%H:%M")
                rem_time = rem_time.replace(year=now.year, month=now.month, day=now.day)
                diff = rem_time - now
                if diff.total_seconds() > 0:
                    mins, secs = divmod(int(diff.total_seconds()), 60)
                    hours, mins = divmod(mins, 60)
                    display += f"🕐 <b>{r['title']}</b> in {hours}h {mins}m {secs}s<br>"
                else:
                    display += f" <b>{r['title']}</b> - time passed.<br>"

        self.setText(display)


class StatsChart(QChartView):
    def __init__(self):
        series = QPieSeries()
        series.append("Health", 60)
        series.append("Safety", 40)

        # Set colors
        series.slices()[0].setBrush(Qt.darkGreen)
        series.slices()[1].setBrush(Qt.red)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Health & Safety Overview")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(Qt.black)
        chart.setTitleBrush(Qt.white)
        chart.legend().setLabelBrush(Qt.white)
        chart.legend().setAlignment(Qt.AlignBottom)

        super().__init__(chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.setMinimumHeight(220)
        self.setStyleSheet("border-radius: 16px; background-color: #0d0d1a;")


class ElderCareGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ElderCareAI Monitor")
        self.setGeometry(100, 100, 680, 650)

        self.health_agent = HealthMonitorAgent()
        self.safety_agent = SafetyAgent()

        self.setStyleSheet(self.dark_theme())

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel("ElderCareAI Monitor")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #D9B0FF; padding: 10px; font-family: 'Poppins';")
        self.layout.addWidget(self.title_label)

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.health_button = QPushButton("Run Health Check")
        self.health_button.setFixedWidth(200)
        self.health_button.setStyleSheet(self.button_style())
        self.health_button.clicked.connect(self.run_health_check)

        self.safety_button = QPushButton("Run Safety Check")
        self.safety_button.setFixedWidth(200)
        self.safety_button.setStyleSheet(self.button_style())
        self.safety_button.clicked.connect(self.run_safety_check)

        self.button_layout.addWidget(self.health_button)
        self.button_layout.addSpacing(20)
        self.button_layout.addWidget(self.safety_button)
        self.layout.addLayout(self.button_layout)

        self.card = FlipCard()
        self.layout.addWidget(self.card)

        self.reminder_box = ReminderBox()
        self.layout.addWidget(self.reminder_box)

        self.chart = StatsChart()
        self.layout.addWidget(self.chart)

        self.setLayout(self.layout)

    def run_health_check(self):
        alerts = self.health_agent.run()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if alerts:
            text = "<b>Health Alerts:</b><br>" + "<br>".join(alerts) + f"<br><i>Last updated: {timestamp}</i>"
        else:
            text = f"No health issues detected.<br><i>Last updated: {timestamp}</i>"
        self.card.update_content(text)

    def run_safety_check(self):
        alerts = self.safety_agent.run()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if alerts:
            text = "<b>Safety Alerts:</b><br>" + "<br>".join(alerts) + f"<br><i>Last updated: {timestamp}</i>"
        else:
            text = f"No safety issues detected.<br><i>Last updated: {timestamp}</i>"
        self.card.update_content(text)

    def dark_theme(self):
        return """
            QWidget {
                background-color: #1e1e2f;
            }
            QLabel {
                color: #D9D9D9;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: rgb(100, 61, 136);
                color: rgb(217, 176, 255);
                font-size: 15px;
                font-weight: bold;
                padding: 12px 30px;
                border: 4px solid rgb(217, 176, 255);
                border-radius: 16px;
                font-family: 'Poppins';
            }
            QPushButton:hover {
                background-color: rgb(217, 176, 255);
                color: rgb(100, 61, 136);
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ElderCareGUI()
    window.show()
    sys.exit(app.exec_())
