# Defines how log files will be cleaned logs older than 7-days on every app startup.

import json
from datetime import datetime, timedelta
import os

LOG_FILE = "../data/prediction_log.jsonl"

def cleanup_old_logs(retention_days=7):
    if not os.path.exists(LOG_FILE):
        return

    try:
        with open(LOG_FILE, "r") as f:
            logs = [json.loads(line) for line in f]

        cutoff = datetime.now() - timedelta(days=retention_days)
        recent_logs = [log for log in logs if datetime.fromisoformat(log["timestamp"]) >= cutoff]

        with open(LOG_FILE, "w") as f:
            for log in recent_logs:
                f.write(json.dumps(log) + "\n")

        print(f"Cleaned up logs. Kept {len(recent_logs)} entries from the last {retention_days} days.")
    except Exception as e:
        print("Failed to clean logs:", e)
