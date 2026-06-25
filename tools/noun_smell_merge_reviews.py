"""Merge subagent noun-smell review files into the candidate dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--review", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    candidates = json.loads(args.candidates.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in candidates}

    merged = 0
    missing: list[str] = []
    for review_path in args.review:
        reviews = json.loads(review_path.read_text(encoding="utf-8"))
        for review in reviews:
            item = by_id.get(review.get("id"))
            if item is None:
                missing.append(str(review.get("id")))
                continue
            item["classifier_label"] = review.get("label", "")
            item["classifier_reason"] = review.get("reason", "")
            item["classifier_rewrite"] = review.get("rewrite", "")
            merged += 1

    args.out.write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    print(f"merged {merged} review records into {args.out}")
    if missing:
        print("missing candidate ids:")
        for item_id in missing:
            print(f"- {item_id}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
