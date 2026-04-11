from .models import Email

TASKS = [
    {
        "id": 0,
        "difficulty": "easy",
        "email": Email(
            subject="Win FREE iPhone!!!",
            body="Click this link to claim your prize now."
        ),
        "expected": "ignore"
    },
    {
        "id": 1,
        "difficulty": "medium",
        "email": Email(
            subject="Meeting Request",
            body="Can we schedule a meeting tomorrow at 10 AM?"
        ),
        "expected": "reply"
    },
    {
        "id": 2,
        "difficulty": "hard",
        "email": Email(
            subject="URGENT: Server Down",
            body="Production server is down. Immediate action needed!"
        ),
        "expected": "mark_urgent"
    }
]
