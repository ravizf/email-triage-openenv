import json
import os


LOG_FILE = "logs.json"


def log_result(task_id, email, action, reward):
    log_entry = {
        "task_id": task_id,
        "subject": email.subject,
        "action": action.action_type,
        "response": action.response,
        "reason": action.reason,
        "confidence": action.confidence,
        "reward": reward,
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
