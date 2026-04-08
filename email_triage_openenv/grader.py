def keyword_score(text, keywords):
    text = text.lower()
    matches = sum(1 for k in keywords if k in text)
    return matches / len(keywords)


def grade(task, action, step):
    expected = task["expected"]

    # Base score
    score = 0.0

    # Correct action
    if action.action_type == expected:
        score += 0.6

    # Keyword understanding
    email_text = task["email"].subject + " " + task["email"].body
    score += 0.3 * keyword_score(email_text, task["keywords"])

    # Response quality (for reply tasks)
    if expected == "reply" and action.response:
        if len(action.response.split()) > 3:
            score += 0.1

    # Penalty for wrong urgent handling
    if expected == "mark_urgent" and action.action_type != "mark_urgent":
        score -= 0.2

    return max(0.0, min(score, 1.0))