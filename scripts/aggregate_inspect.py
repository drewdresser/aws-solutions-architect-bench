#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.10"
# dependencies    = ["pandas", "inspect_ai"]
# ///
"""
Aggregate Inspect `.eval` (or `.json`) logs into a leaderboard CSV.

Examples
--------
# gather every log under ./logs into results/leaderboard.csv
uv run --script scripts/aggregate_inspect.py --log-dir ./logs

# explicitly pass individual files
./scripts/aggregate_inspect.py logs/*gpt4o.eval
"""

from __future__ import annotations

import argparse
import pathlib
from typing import Sequence

import pandas as pd
from inspect_ai.log import (
    list_eval_logs,
    read_eval_log,  # fast header-only read
    read_eval_log_sample_summaries,  # per-sample summaries
)


def _accuracy_from_log(log_path: str) -> tuple[str, int, int]:
    """Return (model, correct, total) for one log."""
    hdr = read_eval_log(log_path, header_only=True)
    model = hdr.eval.model if isinstance(hdr.eval.model, str) else hdr.eval.model.name

    # Prefer aggregated accuracy if scorer already computed it
    if hdr.results and hdr.results.scores:
        # Use the total_samples from results
        total = hdr.results.total_samples
        # Extract mean accuracy from the first score's metrics
        first_score = hdr.results.scores[0]
        if first_score.metrics and "mean" in first_score.metrics:
            accuracy = first_score.metrics["mean"].value
            correct = round(accuracy * total)
            return model, correct, total

    # Otherwise compute pass-rate from sample summaries
    correct = 0
    samples = read_eval_log_sample_summaries(log_path)
    for s in samples:
        # Each scorer attaches its metrics under s.scores (a dict[str, Score])
        # We handle the cdk_verify scoring system that uses 'C' for correct, 'I' for incorrect
        if s.scores:
            for name, metric in s.scores.items():
                val = getattr(metric, "value", metric)  # Score → scalar
                # Check for 'C' (correct) or traditional pass/boolean values
                if val == "C" or name == "pass" or val in (0, 1, True, False):
                    if val == "C" or (name == "pass" and val) or val in (1, True):
                        correct += 1
                    break
    return model, correct, len(samples)


def collect(log_files: Sequence[str]) -> pd.DataFrame:
    rows = [_accuracy_from_log(p) for p in log_files]
    df = pd.DataFrame(rows, columns=["model", "correct", "total"])
    df["accuracy"] = (df.correct / df.total).round(4)
    return df.sort_values("accuracy", ascending=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log-dir", help="Directory of Inspect logs")
    ap.add_argument("logs", nargs="*", help="One or more .eval / .json logs")
    ap.add_argument("--outfile", default="results/leaderboard.csv")
    args = ap.parse_args()

    # Resolve the list of files
    if args.logs:
        files = [str(pathlib.Path(f)) for f in args.logs]
    elif args.log_dir:
        log_infos = list_eval_logs(args.log_dir)
        files = [str(log_info.name) for log_info in log_infos]
    else:
        raise SystemExit("Specify --log-dir or pass log files")

    if not files:
        raise SystemExit("No log files found.")

    leaderboard = collect(files)
    pathlib.Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)
    leaderboard.to_csv(args.outfile, index=False)
    print(f"🏁  Leaderboard written → {args.outfile}\n")
    print(leaderboard.to_string(index=False))


if __name__ == "__main__":
    main()
