from __future__ import annotations

import argparse
import json
from pathlib import Path

from .store import MilestoneStore


def main() -> None:
    p = argparse.ArgumentParser(description="Milestones CLI")
    p.add_argument("--data", type=str, default=str(Path(__file__).resolve().parents[2] / "data" / "milestones"))
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("list-stages")
    s1.add_argument("--include-noisy", action="store_true")

    s2 = sub.add_parser("milestones")
    s2.add_argument("age_months", type=int)
    s2.add_argument("--include-noisy", action="store_true")

    args = p.parse_args()
    store = MilestoneStore(Path(args.data))

    if args.cmd == "list-stages":
        stages = [s.__dict__ for s in store.stages if args.include_noisy or not s.is_noisy]
        print(json.dumps(stages, indent=2))
        return

    if args.cmd == "milestones":
        ms = [m.__dict__ for m in store.milestones_for_age(args.age_months, include_noisy=args.include_noisy)]
        print(json.dumps(ms, indent=2))
        return


if __name__ == "__main__":
    main()
