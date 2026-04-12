---
title: Email Triage OpenEnv
emoji: "📧"
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Email Triage OpenEnv

This project implements a real-world email triage environment where an agent classifies emails into one of three actions:

- ignore
- reply
- mark_urgent

## Features

- step / reset / state environment API
- 3 tasks with increasing difficulty
- deterministic partial-reward grader
- lightweight local web UI
- validator-friendly inference script

## Tasks

1. Easy: spam email -> ignore
2. Medium: meeting request -> reply
3. Hard: urgent server issue -> mark_urgent

## Run locally

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:7860`.

## Run inference

```bash
python inference.py
```

## Docker

```bash
docker build -t email-env .
docker run -p 7860:7860 email-env
```

## What to do now

Run these commands:

```bash
git add .
git commit -m "Fix phase 2 task grading with partial rewards"
git push
```

Then wait for GitHub and Hugging Face to update, and resubmit.

The key fix here is:

- 3 tasks exist
- every task has a grader
- scores are strictly between 0 and 1
- no 0.0
- no 1.0
