# Defines how the notifications will pop-up if an emotion is flagged as risky.

import time
import datetime
import json
import os
import threading
from plyer import notification

PREDICTION_LOG_PATH = "./data/prediction_log.jsonl"

# thresholds for triggering notifications
DISTRESS_THRESHOLD = 0.8
POSITIVE_THRESHOLD = 0.85

enable_distress_alerts = True
enable_daily_reminder = True
LAST_CHECKIN_DATE = None

def send_notification(title, message, callback_url=None):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # seconds
    )

def read_latest_log():
    if not os.path.exists(PREDICTION_LOG_PATH):
        return None
    with open(PREDICTION_LOG_PATH, "r") as f:
        lines = f.readlines()
        if not lines:
            return None
        return json.loads(lines[-1])

def check_for_distress():
    last_alert_time = None
    while True:
        log = read_latest_log()
        if log:
            label = log["result"].get("label")
            score = log["result"].get("score", 0)

            if enable_distress_alerts and label.lower() in ["sad", "anger", "anxious", "distress"] and score >= DISTRESS_THRESHOLD:
                # avoid repeating notification too frequently
                if not last_alert_time or (datetime.datetime.now() - last_alert_time).seconds > 600:
                    send_notification(
                        "🚨 Distress Detected!",
                        "Would you like to try some breathing exercises? Head to the Exercises tab for help."
                    )
                    last_alert_time = datetime.datetime.now()
        time.sleep(10)

def send_daily_checkin():
    global LAST_CHECKIN_DATE
    while True:
        now = datetime.datetime.now()
        if enable_daily_reminder:
            if LAST_CHECKIN_DATE != now.date():
                # setting for same time everyday e.g., 8 PM
                if now.hour == 20 and now.minute == 0:
                    send_notification(
                        "📊 Time for your Daily Mental Health Check-in!",
                        "Click to open your dashboard."
                    )
                    LAST_CHECKIN_DATE = now.date()
        time.sleep(60)


def start_notification_threads():
    threading.Thread(target=check_for_distress, daemon=True).start()
    threading.Thread(target=send_daily_checkin, daemon=True).start()


if __name__ == "__main__":
    print("Starting notification system...")
    start_notification_threads()
    while True:
        time.sleep(1)
