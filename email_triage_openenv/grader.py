def _extract_prediction(*args, **kwargs):
    if "prediction" in kwargs and "ground_truth" in kwargs:
        return kwargs["prediction"], kwargs["ground_truth"]

    if "task" in kwargs and "action" in kwargs:
        task = kwargs["task"]
        action = kwargs["action"]
        return getattr(action, "action_type", action), task.get("expected")

    if len(args) == 2:
        first, second = args
        if isinstance(first, dict):
            return getattr(second, "action_type", second), first.get("expected")
        return first, second

    return None, None


def grade(task, action=None):
    predicted, expected = _extract_prediction(task, action) if action is not None else _extract_prediction(task)

    if predicted is None or expected is None:
        return 0.01

    predicted = str(predicted).strip().lower()
    expected = str(expected).strip().lower()

    if predicted == expected:
        return 0.9

    if expected == "mark_urgent":
        if predicted == "reply":
            return 0.6
        if predicted == "ignore":
            return 0.2
        return 0.1

    if expected == "reply":
        if predicted == "mark_urgent":
            return 0.5
        if predicted == "ignore":
            return 0.2
        return 0.1

    if expected == "ignore":
        if predicted == "reply":
            return 0.4
        if predicted == "mark_urgent":
            return 0.3
        return 0.1

    return 0.1


def grade_task_0(*args, **kwargs):
    predicted, _ = _extract_prediction(*args, **kwargs)
    return grade(predicted or "ignore", "ignore")


def grade_task_1(*args, **kwargs):
    predicted, _ = _extract_prediction(*args, **kwargs)
    return grade(predicted or "ignore", "reply")


def grade_task_2(*args, **kwargs):
    predicted, _ = _extract_prediction(*args, **kwargs)
    return grade(predicted or "ignore", "mark_urgent")


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
