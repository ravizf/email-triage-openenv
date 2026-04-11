def grade(task, action):
    expected = task["expected"]
    predicted = action.action_type

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
