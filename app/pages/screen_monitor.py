# Defines the functions which will enable capturing screenshots of allowed windows which will be converted into text

import pytesseract
import datetime
import pygetwindow as gw
from PIL import ImageGrab
import json
import time

from predict_pipeline import analyze_text

log_file = "../data/prediction_log.jsonl"

def get_open_windows():
    return list(set([w.title for w in gw.getWindowsWithTitle("") if w.title.strip()]))

def get_active_window():
    try:
        return gw.getActiveWindow().title
    except:
        return "Unknown"

def capture_and_analyze(whitelist):
    timestamp = datetime.datetime.now().isoformat()
    title = get_active_window()

    if any(app in title for app in whitelist):
        img = ImageGrab.grab()
        text = pytesseract.image_to_string(img)

        if text.strip():
            prediction = analyze_text(text)
            log = {
                "timestamp": timestamp,
                "window": title,
                "text": text[:200],
                "result": prediction
            }

            with open(log_file, "a") as f:
                f.write(json.dumps(log) + "\n")

            print(f"[{timestamp}] Monitored: {title}")

def start_monitoring(whitelist, stop_flag):
    while not stop_flag["stop"]:
        capture_and_analyze(whitelist)
        time.sleep(10)