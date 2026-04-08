def llm_decide(email):
    text = (email.subject + " " + email.body).lower()

    if any(word in text for word in ["urgent", "server", "crash", "asap", "down"]):
        return {
            "action": "mark_urgent",
            "response": "",
            "reason": "Detected urgent/system-failure keywords",
            "confidence": 0.92,
        }

    elif any(word in text for word in ["meeting", "schedule", "tomorrow", "request"]):
        return {
            "action": "reply",
            "response": "Sure, I am available for the meeting.",
            "reason": "Detected meeting/scheduling keywords",
            "confidence": 0.87,
        }

    elif any(word in text for word in ["free", "win", "lottery", "click", "prize"]):
        return {
            "action": "ignore",
            "response": "",
            "reason": "Detected spam/promotional keywords",
            "confidence": 0.84,
        }

    else:
        return {
            "action": "ignore",
            "response": "",
            "reason": "No important keywords detected",
            "confidence": 0.65,
        }
