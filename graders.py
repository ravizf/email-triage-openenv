def _normalize_reward(reward):
    return min(max(float(reward), 0.01), 0.99)


def grade_task_0(state, reward):
    task_id = state.get("task_id")
    return _normalize_reward(reward if int(task_id) == 0 else 0.01)


def grade_task_1(state, reward):
    task_id = state.get("task_id")
    return _normalize_reward(reward if int(task_id) == 1 else 0.01)


def grade_task_2(state, reward):
    task_id = state.get("task_id")
    return _normalize_reward(reward if int(task_id) == 2 else 0.01)


GRADERS = {
    "email_triage_task_0": grade_task_0,
    "email_triage_task_1": grade_task_1,
    "email_triage_task_2": grade_task_2,
}

TASK_GRADER_PAIRS = [
    ("email_triage_task_0", grade_task_0),
    ("email_triage_task_1", grade_task_1),
    ("email_triage_task_2", grade_task_2),
]

__all__ = [
    "grade_task_0",
    "grade_task_1",
    "grade_task_2",
    "GRADERS",
    "TASK_GRADER_PAIRS",
]
