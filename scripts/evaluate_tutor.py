"""Reproducible, illustrative evaluation of CodeMind's deterministic diagnoses.

Run from repository root: python scripts/evaluate_tutor.py
The labeled scenarios are authored probes, not a representative learner dataset.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.catalog import EXERCISES  # noqa: E402
from backend.tutor import diagnose  # noqa: E402

CASES = [
    ("passed", "sum-list", "def sum_list(xs):\n return sum(xs)", {"status":"completed","tests":[{"passed":True,"expected":3,"actual":3}]}),
    ("missing_return", "sum-list", "def sum_list(xs):\n total=0\n for x in xs: total+=x", {"status":"completed","tests":[{"passed":False,"expected":3,"actual":None}]}),
    ("loop_boundary", "fibonacci", "def fibonacci(n):\n s=0\n for i in range(n): s+=i\n return s", {"status":"completed","tests":[{"passed":False,"expected":3,"actual":2}]}),
    ("wrong_output", "is-even", "def is_even(n):\n return n%2==1", {"status":"completed","tests":[{"passed":False,"expected":True,"actual":False}]}),
    ("syntax_error", "sum-list", "def sum_list(:", {"status":"syntax_error","message":"invalid syntax"}),
    ("runtime_error", "find-largest", "def find_largest(xs):\n return xs[9]", {"status":"runtime_error","message":"IndexError: list index out of range"}),
]

def main() -> None:
    catalog = {e["id"]: e for e in EXERCISES}
    counts = Counter((e["category"], e["difficulty"]) for e in EXERCISES)
    outputs=[]
    for label, eid, code, run in CASES:
        result=diagnose(catalog[eid], code, run)
        outputs.append({"label":label,"exercise_id":eid,"diagnosis":result["title"],"category":result["category"],"confidence":result["confidence"],"evidence":result["evidence"]})
    matrix=Counter((x["label"],x["diagnosis"]) for x in outputs)
    out={"kind":"authored_probe_not_learner_dataset","exercise_count":len(EXERCISES),"category_difficulty_counts":[{"category":k[0],"difficulty":k[1],"count":v} for k,v in sorted(counts.items())],"scenarios":outputs,"diagnosis_title_counts":dict(Counter(x["diagnosis"] for x in outputs)),"note":"No accuracy/precision/recall/F1 is reported: labels describe scenario types while the tutor emits free-form diagnostic titles, so a valid mapping requires expert adjudication and a larger held-out set."}
    path=ROOT/"reports"/"evaluation_results.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps(out,indent=2))

if __name__ == "__main__": main()
