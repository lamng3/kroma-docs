#!/usr/bin/env python3
"""Export KROMA's published results for the manual's arena page.

    python3 leaderboard_data.py [../kroma/README.md]

Reads the three F1 tables of the README (Table 3 of the paper): KROMA against the best baseline, the ablations, and the
other language models. One board per track; the page ranks the rows by F1 and computes nothing else.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
README = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / "kroma/README.md")


def number(text):
    m = re.search(r"\d+\.\d+", text)
    return float(m.group(0)) if m else None


def tag(text):
    m = re.search(r"<sub>(.*?)</sub>", text)
    return m.group(1) if m else ""


def tables(text):
    out, block = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            block.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif block:
            out.append(block)
            block = []
    return out


def main():
    results = README.read_text().split("## 📊 Results")[1].split("\n## ")[0]
    by_header = {tuple(t[0]): t[2:] for t in tables(results)}
    main_rows = next(v for k, v in by_header.items() if k[:3] == ("Track", "KROMA", "Best baseline"))
    ablation = next(v for k, v in by_header.items() if "without refinement" in k)
    models = next(v for k, v in by_header.items() if "Qwen2.5-1.5B" in k)
    rows = {}
    for track, kroma, base in main_rows:
        rows.setdefault(track, []).append({"name": "KROMA", "group": "kroma", "tag": tag(kroma) or "Llama-3.3-70B", "score": number(kroma)})
        rows[track].append({"name": tag(base), "group": "baseline", "tag": "best published baseline", "score": number(base)})
    for track, _, no_retrieval, no_refine in ablation:
        rows[track].append({"name": "KROMA without retrieval", "group": "ablation", "tag": "Llama-3.3-70B", "score": number(no_retrieval)})
        rows[track].append({"name": "KROMA without refinement", "group": "ablation", "tag": "Llama-3.3-70B", "score": number(no_refine)})
    for track, small, gpt, llama in models:
        have = {(r["name"], r["tag"]) for r in rows[track]}
        for model, score in (("Qwen2.5-1.5B", small), ("GPT-4o-mini", gpt), ("Llama-3.3-70B", llama)):
            if ("KROMA", model) not in have:
                rows[track].append({"name": f"KROMA with {model}", "group": "kroma", "tag": "smaller or cheaper model", "score": number(score)})
    boards = [
        {"id": t, "name": t, "sub": f"{t}: F1 (%) of the alignment, from Table 3 of the paper.", "metric": "f1", "metricLabel": "F1 (%)", "fmt": "f2",
         "columns": [], "rows": r}
        for t, r in rows.items()
    ]
    out = {
        "note": "F1 (%) as published in the paper (full.pdf, Table 3) and the README. KROMA uses Llama-3.3-70B unless a row says otherwise; baselines are MILA, OLaLa, and LLM4OM with their reported models, each row showing the best of them on that track.",
        "groups": {"kroma": {"label": "KROMA", "ours": True}, "ablation": {"label": "Ablation"}, "baseline": {"label": "Baseline"}},
        "boards": boards,
    }
    (ROOT / "leaderboard-data.json").write_text(json.dumps(out))
    print(", ".join(f"{b['id']}: {len(b['rows'])}" for b in boards))


if __name__ == "__main__":
    main()
