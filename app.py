from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from email_triage_openenv.env import EmailTriageEnv
from email_triage_openenv.models import Action
from llm_agent import llm_decide


env = EmailTriageEnv()


def run_agent(task_id):
    try:
        task_id = int(task_id)
    except (TypeError, ValueError):
        return "Invalid task ID. Use 0, 1, or 2."

    if task_id not in [0, 1, 2]:
        return "Invalid task ID. Use 0, 1, or 2."

    obs = env.reset(task_id)
    result = llm_decide(obs.email)

    action = Action(
        action_type=result.get("action", "ignore"),
        response=result.get("response", ""),
        reason=result.get("reason", ""),
        confidence=result.get("confidence", 0.0),
    )

    _, reward, _, _ = env.step(action)

    return "\n".join(
        [
            f"Subject: {obs.email.subject}",
            f"Body: {obs.email.body}",
            "",
            f"Action: {action.action_type}",
            f"Response: {action.response}",
            "",
            f"Reason: {action.reason}",
            f"Confidence: {round(action.confidence, 2)}",
            f"Score: {round(reward, 2)}",
        ]
    )


def render_page(output=""):
    escaped_output = escape(output)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Email Triage OpenEnv</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            padding: 32px 16px;
            color: #1f2937;
        }}
        .card {{
            max-width: 760px;
            margin: 0 auto;
            background: #ffffff;
            padding: 32px;
            border-radius: 16px;
            box-shadow: 0 12px 32px rgba(15, 23, 42, 0.12);
        }}
        h1 {{
            margin-top: 0;
            font-size: 32px;
        }}
        p {{
            line-height: 1.5;
        }}
        label {{
            display: block;
            font-weight: 600;
            margin: 20px 0 8px;
        }}
        input {{
            width: 100%;
            padding: 14px;
            font-size: 16px;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            box-sizing: border-box;
        }}
        button {{
            margin-top: 16px;
            background: #2563eb;
            color: white;
            border: 0;
            border-radius: 10px;
            padding: 14px 20px;
            font-size: 16px;
            cursor: pointer;
        }}
        pre {{
            margin-top: 24px;
            background: #0f172a;
            color: #e2e8f0;
            padding: 18px;
            border-radius: 12px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        .hint {{
            color: #475569;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>AI Email Triage System</h1>
        <p>Rule-based email triage environment with explanation and confidence.</p>
        <form method="post">
            <label for="task_id">Enter Task ID</label>
            <input id="task_id" name="task_id" type="number" min="0" max="2" placeholder="0, 1, or 2" required>
            <div class="hint">Use task 0 for spam, 1 for meeting request, and 2 for urgent incident.</div>
            <button type="submit">Submit</button>
        </form>
        <pre>{escaped_output or "Output will appear here."}</pre>
    </div>
</body>
</html>"""


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        page = render_page()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length).decode("utf-8")
        form_data = parse_qs(raw_body)
        task_id = form_data.get("task_id", [""])[0]
        output = run_agent(task_id)
        page = render_page(output)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def log_message(self, format, *args):
        return


def main():
    server = HTTPServer(("0.0.0.0", 7860), AppHandler)
    print("Server running at http://127.0.0.1:7860")
    server.serve_forever()


if __name__ == "__main__":
    main()
