#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "pandas>=2.2",
#   "inspect_ai>=0.3.46"
# ]
# ///
"""
aggregate_multi.py — Build a multi-column leaderboard from Inspect logs.

Usage
-----
uv run --script scripts/aggregate_multi.py --log-dir logs \
        --outfile results/leaderboard.csv \
        --json-out  results/leaderboard.json
"""

from __future__ import annotations

import argparse, pathlib, math, json
from typing import Any, Dict, List, Union, Optional
import pandas as pd  # type: ignore
from inspect_ai.log import list_eval_logs, read_eval_log_sample_summaries, read_eval_log
from task_registry import TASKS


def scores_to_dict(scores_obj: Any) -> Dict[str, Any]:
    """
    Normalise Inspect's score payload to {name: score_obj}.
    Handles dict, list[Score], list[dict], or None.
    """
    if isinstance(scores_obj, dict):
        return scores_obj
    if isinstance(scores_obj, list):
        out = {}
        for s in scores_obj:
            name = getattr(s, "name", None) or (
                s.get("name") if isinstance(s, dict) else None
            )
            if name:
                out[name] = s
        return out
    return {}


def detect_task_key(path: str) -> Optional[str]:
    """Return TASK key for this log, or None if no match."""
    # 1) filename / folder substring
    path_str = str(path)
    for key, cfg in TASKS.items():
        patterns = list(cfg.get("patterns", []))
        if patterns and any(p in path_str for p in patterns):
            return key

    # 2) fallback: inspect the dataset-id stored in the header
    try:
        hdr = read_eval_log(path, header_only=True)
        ds_id = str(getattr(hdr.eval, "dataset", ""))
        for key, cfg in TASKS.items():
            fallback_patterns = list(cfg.get("patterns", []))
            if fallback_patterns and any(p in ds_id for p in fallback_patterns):
                return key
    except Exception:
        pass

    return None


def metric_value(sample: Any, task_cfg: Dict[str, Any]) -> float:
    """Extract metric value from sample based on task configuration.

    Supports:
    - Multiple choice (choice): returns 1.0 if correct else 0.0
    - CDK verify (cdk_verify): returns 1.0 if value in pass_values else 0.0
    - Numeric rubric scores (e.g., architecture_scorer): returns the float value in [0,1]
    """
    raw = getattr(sample, "scores", None) or getattr(sample, "score", None)
    scores = scores_to_dict(raw)
    metric_name = task_cfg["metric"]

    if metric_name not in scores:
        raise KeyError(f"{metric_name} not in {list(scores.keys())}")

    m = scores[metric_name]

    # Handle different score formats
    if isinstance(m, dict):
        # For dict-based scores, get the "value" key
        v = m.get("value", m)
    else:
        # For object-based scores, get the value attribute
        v = getattr(m, "value", m)

    # CDK verifier: check if value is in pass_values (prioritize this over multiple choice)
    if "pass_values" in task_cfg:
        pass_values = task_cfg["pass_values"]
        return float(v in pass_values)

    # Numeric rubric values: if v is numeric, return as-is (assumed in [0,1])
    if isinstance(v, (int, float)):
        return float(v)

    # Multiple-choice format (only if not CDK verifier)
    if isinstance(m, dict) and "answer" in m:
        return float(m.get("value") == m.get("answer"))

    # Check if it's a Score object with answer attribute
    if hasattr(m, "answer") and hasattr(m, "value"):
        answer = getattr(m, "answer", None)
        value = getattr(m, "value", None)
        if answer is not None:
            return float(value == answer)

    # Default: convert to boolean
    return float(bool(v))


def summarise_log(path: str) -> Optional[Dict[str, Any]]:
    """Return dict: {'task': …, 'model': …, 'accuracy': …} for one file."""
    # Detect task by registry pattern
    task_key = detect_task_key(path)
    if task_key is None:
        print(f"[warn] Skipping {path} — no TASK pattern match")
        return None

    task_cfg = TASKS[task_key]

    # Pull per-sample scores
    samples = read_eval_log_sample_summaries(path)
    if not samples:
        return None

    metric = task_cfg["metric"]
    norm = task_cfg.get("normalizer", 1)
    # Ensure norm is an integer
    if not isinstance(norm, int):
        norm = 1

    # Process all samples
    all_vals = [metric_value(s, task_cfg) for s in samples]

    # Boolean pass/fail or numeric rubric → accuracy in [0,1]
    acc = sum(all_vals) / (len(all_vals) * norm)

    model = getattr(samples[0], "model", None) or "unknown"

    if not model or model == "unknown":
        try:
            hdr = read_eval_log(path, header_only=True)
            model = str(getattr(hdr.eval, "model", "unknown"))
        except Exception as e:
            pass

    return {"task": task_key, "model": model, "accuracy": round(acc, 4)}


def collect(files: List[str]) -> pd.DataFrame:
    rows = filter(None, (summarise_log(f) for f in files))
    df = pd.DataFrame(rows)

    if df.empty:
        raise SystemExit("No valid logs found")

    # Handle duplicate entries by aggregating them (take mean accuracy)
    # This prevents pivot errors when there are multiple logs for the same model+task
    df_agg = df.groupby(["model", "task"], as_index=False)["accuracy"].mean()

    # pivot: one row per model, one col per task
    table = df_agg.pivot(index="model", columns="task", values="accuracy").fillna(0)

    # weighted overall
    for t, cfg in TASKS.items():
        if t not in table.columns:
            table[t] = 0
    table["overall"] = sum(table[t] * cfg["weight"] for t, cfg in TASKS.items()).round(
        4
    )

    return table.reset_index()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--log-dir", required=True)
    ap.add_argument("--outfile", default="results/leaderboard.csv")
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()

    logs = list_eval_logs(args.log_dir)
    log_paths = [str(log.name) for log in logs]
    leaderboard = collect(log_paths)

    pathlib.Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)
    leaderboard.to_csv(args.outfile, index=False)
    print(f"CSV leaderboard → {args.outfile}")
    print(leaderboard.to_string(index=False))

    if args.json_out:
        leaderboard.to_json(args.json_out, orient="records", indent=2)
        print(f"JSON leaderboard → {args.json_out}")


if __name__ == "__main__":
    main()
