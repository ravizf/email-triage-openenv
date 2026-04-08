import json
import os

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer


def generate_report():
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Email Triage Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph("Performance Summary", styles["Heading2"]),
        Spacer(1, 12),
    ]

    if os.path.exists("logs.json"):
        with open("logs.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        content.append(Paragraph(f"Total runs: {len(data)}", styles["BodyText"]))
        if data:
            average_score = sum(entry["reward"] for entry in data) / len(data)
            content.append(Spacer(1, 8))
            content.append(
                Paragraph(f"Average score: {average_score:.2f}", styles["BodyText"])
            )
            content.append(Spacer(1, 12))

    if os.path.exists("performance.png"):
        content.append(Image("performance.png"))

    doc.build(content)
