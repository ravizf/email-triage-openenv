TASKS = [
    {
        "id": "email_triage_task_0",
        "task_id": "spam_filter",
        "name": "spam-filter",
        "difficulty": "easy",
        "description": "Classify a promotional spam email and ignore it.",
        "max_steps": 1,
        "reset_params": {"task_id": 0},
        "action_schema": {
            "action_type": "ignore",
            "task_id": "spam_filter",
        },
        "grader": "graders:grade_task_0",
        "graders": ["graders:grade_task_0"],
        "reward_range": [0.01, 0.99],
    },
    {
        "id": "email_triage_task_1",
        "task_id": "meeting_reply",
        "name": "meeting-reply",
        "difficulty": "medium",
        "description": "Classify a meeting request and reply appropriately.",
        "max_steps": 1,
        "reset_params": {"task_id": 1},
        "action_schema": {
            "action_type": "reply",
            "task_id": "meeting_reply",
        },
        "grader": "graders:grade_task_1",
        "graders": ["graders:grade_task_1"],
        "reward_range": [0.01, 0.99],
    },
    {
        "id": "email_triage_task_2",
        "task_id": "urgent_incident",
        "name": "urgent-incident",
        "difficulty": "hard",
        "description": "Classify an urgent production incident and mark it urgent.",
        "max_steps": 1,
        "reset_params": {"task_id": 2},
        "action_schema": {
            "action_type": "mark_urgent",
            "task_id": "urgent_incident",
        },
        "grader": "graders:grade_task_2",
        "graders": ["graders:grade_task_2"],
        "reward_range": [0.01, 0.99],
    },
]

TASK_ID_TO_INDEX = {
    "spam_filter": 0,
    "meeting_reply": 1,
    "urgent_incident": 2,
}

TASK_GRADER_PAIRS = [
    ("email_triage_task_0", "graders:grade_task_0"),
    ("email_triage_task_1", "graders:grade_task_1"),
    ("email_triage_task_2", "graders:grade_task_2"),
]

__all__ = ["TASKS", "TASK_ID_TO_INDEX", "TASK_GRADER_PAIRS"]
