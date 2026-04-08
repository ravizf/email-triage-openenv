import json
import os

import matplotlib.pyplot as plt


def generate_chart(log_file="logs.json", output_file="performance.png"):
    if not os.path.exists(log_file):
        return

    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        return

    scores = [entry["reward"] for entry in data]
    runs = list(range(1, len(scores) + 1))

    plt.figure(figsize=(7, 4))
    plt.plot(runs, scores, marker="o", linewidth=2)
    plt.title("Agent Performance")
    plt.xlabel("Run")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.xticks(runs)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
