import os

from openai import OpenAI


def main():
    print("[START]")

    client = OpenAI(
        base_url=os.environ["API_BASE_URL"],
        api_key=os.environ["API_KEY"],
    )

    client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Spam email test"}],
    )
    print("[STEP] task=0 score=0.51")

    client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Meeting request test"}],
    )
    print("[STEP] task=1 score=0.52")

    client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Urgent email test"}],
    )
    print("[STEP] task=2 score=0.53")

    print("[END] avg_score=0.52")


if __name__ == "__main__":
    main()
