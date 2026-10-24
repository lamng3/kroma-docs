#!/usr/bin/env python3
"""Export what the KROMA playground needs from the real code.

    ../kroma/.venv/bin/python playground_data.py

The prompt templates of kroma.tasks.prompts (so the page builds prompts from the same text), and fixtures that pin the
page's JavaScript ports of answer extraction and voting to kroma.agents.utils. The page's tests compare them.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "kroma" / "src"))

from kroma.agents.utils import extract_confidence, extract_yes_no, majority_vote  # noqa: E402
from kroma.tasks.prompts.templates import SYSTEM_PROMPT, TASK_PROMPT  # noqa: E402

RESPONSES = [
    "<answer>Yes</answer> <confidence>8</confidence>",
    "<answer> no </answer>\n<confidence> 3 </confidence>",
    "<answer>maybe</answer><confidence>7</confidence>",
    "I think so. <answer>YES</answer> <confidence>99</confidence>",
    "no tags at all",
]


def main():
    data = {
        "system": SYSTEM_PROMPT,
        "task": TASK_PROMPT,
        "fixtures": {
            "extract": [{"input": r, "answer": extract_yes_no(r), "confidence": extract_confidence(r)} for r in RESPONSES],
            "vote": {"input": [[1, 8], [1, 6], [0, 9]], "output": list(majority_vote([(1, 8), (1, 6), (0, 9)]))},
        },
    }
    (ROOT / "playground-data.json").write_text(json.dumps(data))
    print("templates and", len(RESPONSES), "extraction fixtures")


if __name__ == "__main__":
    main()
