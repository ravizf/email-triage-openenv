def llm_decide(email):
    text = (email.subject + " " + email.body).lower()

    urgent_keywords = ["urgent", "server", "crash", "asap", "down", "immediate", "production"]
    meeting_keywords = ["meeting", "schedule", "tomorrow", "request", "available"]
    spam_keywords = ["free", "win", "lottery", "click", "prize", "claim"]

    urgent_hits = sum(word in text for word in urgent_keywords)
    meeting_hits = sum(word in text for word in meeting_keywords)
    spam_hits = sum(word in text for word in spam_keywords)

    if urgent_hits >= max(meeting_hits, spam_hits) and urgent_hits > 0:
        return {
            "action": "mark_urgent",
            "response": "",
            "reason": f"Detected {urgent_hits} urgent/system keywords",
            "confidence": min(0.55 + 0.08 * urgent_hits, 0.95)
        }

    if meeting_hits >= max(urgent_hits, spam_hits) and meeting_hits > 0:
        return {
            "action": "reply",
            "response": "Sure, I am available for the meeting.",
            "reason": f"Detected {meeting_hits} meeting/scheduling keywords",
            "confidence": min(0.55 + 0.08 * meeting_hits, 0.92)
        }

    if spam_hits > 0:
        return {
            "action": "ignore",
            "response": "",
            "reason": f"Detected {spam_hits} spam/promotional keywords",
            "confidence": min(0.55 + 0.08 * spam_hits, 0.90)
        }

    return {
        "action": "ignore",
        "response": "",
        "reason": "No strong priority indicators found",
        "confidence": 0.6
    }
