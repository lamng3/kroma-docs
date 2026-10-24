#!/usr/bin/env python3
"""Export real prompts for the manual's live demo.

    RECORDED_RUN=/path/to/run_dir ../kroma/.venv/bin/python demo_data.py

For a sample of Mouse-Human pairs from a recorded run (the directory in RECORDED_RUN) this finds the two classes in
the ontologies, reads their parents and children with kroma's own loader, builds the prompt with kroma's
`build_task_prompt`, and keeps the answer the run recorded. The page shows the prompt and the answer; nothing is
asked of a model in the browser.
"""

import json
import os
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KROMA = ROOT.parent / "kroma"
AO = Path(os.environ.get("RECORDED_RUN", ROOT))
DATA = AO / "data" / "MouseHuman"
sys.path.insert(0, str(KROMA / "src"))
sys.path.insert(0, str(AO / "showcase"))

from rdflib import RDFS, Graph  # noqa: E402

from kroma.tasks.loader import OwlOntologyLoader  # noqa: E402
from kroma.tasks.prompts.builders import build_task_prompt  # noqa: E402


def labels(path, known):
    """label -> class uri, and class uri -> label, for the classes in `known` (blank-node axioms carry labels too)."""
    g = Graph()
    g.parse(path, format="xml")
    by_label, by_uri = {}, {}
    for s, _, o in g.triples((None, RDFS.label, None)):
        if str(s) in known:
            by_label.setdefault(str(o).strip().lower(), str(s))
            by_uri[str(s)] = str(o).strip()
    return by_label, by_uri


def hierarchy(path):
    """parents, children: class uri -> uris, from kroma's loader."""
    graph, _, _ = OwlOntologyLoader(str(path)).load()
    parents, children = defaultdict(set), defaultdict(set)
    for (_, parent), kids in graph.items():
        for _, kid in kids:
            children[parent].add(kid)
            parents[kid].add(parent)
    return parents, children


def context(uri, by_uri, parents, children):
    name = by_uri.get(uri, uri.split("#")[-1])
    par = sorted(by_uri[u] for u in parents.get(uri, ()) if u in by_uri)
    chi = sorted(by_uri[u] for u in children.get(uri, ()) if u in by_uri)
    return (name, par, chi, [], [])


def main():
    import build  # the run's page data, so the decisions match

    run = json.loads((AO / "run.json").read_text())
    decisions = [d for d in build.page_data(run)["decisions"] if d["agent"] == "kroma"]
    mp, mc = hierarchy(DATA / "mouse.owl")
    hp, hc = hierarchy(DATA / "human.owl")
    mouse_label, mouse_by_uri = labels(DATA / "mouse.owl", set(mp) | set(mc))
    human_label, human_by_uri = labels(DATA / "human.owl", set(hp) | set(hc))
    pool = [d for d in decisions if d["s"].lower() in mouse_label and d["c"].lower() in human_label]
    rng = random.Random(1)
    picks = []
    for group_key in sorted({d["tier"] for d in pool}):
        for ok in (True, False):
            group = [d for d in pool if d["tier"] == group_key and d["ok"] == ok and d["verb"]]
            picks += rng.sample(group, min(2 if ok else 1, len(group)))
    out = {"source": "recorded run, 2026-10-18", "pairs": []}
    for d in picks:
        su, tu = mouse_label[d["s"].lower()], human_label[d["c"].lower()]
        source = context(su, mouse_by_uri, mp, mc)
        target = context(tu, human_by_uri, hp, hc)
        system, user = build_task_prompt(source, target)
        out["pairs"].append(
            {
                "source": source[0],
                "target": target[0],
                "context": {"source": list(source), "target": list(target)},
                "system": system.strip(),
                "prompt": user.strip(),
                "answer": d["ans"],
                "confidence": d["conf"],
                "correct": d["ok"],
            }
        )
    (ROOT / "demo-data.json").write_text(json.dumps(out))
    print(f"{len(out['pairs'])} pairs")


if __name__ == "__main__":
    main()
