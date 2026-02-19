from __future__ import annotations

import argparse
import json
from pathlib import Path

from .filters import evaluate_filter
from .parser import parse_item_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="poe2-assistant",
        description="Evaluate copied PoE2 item text against a JSON filter.",
    )
    parser.add_argument("--item-file", type=Path, required=True, help="Path to copied item text file")
    parser.add_argument("--filter-file", type=Path, required=True, help="Path to filter JSON file")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    item_text = args.item_file.read_text(encoding="utf-8")
    filter_config = json.loads(args.filter_file.read_text(encoding="utf-8"))

    item = parse_item_text(item_text)
    result = evaluate_filter(item, filter_config)

    if result.matched:
        print("HIT")
        for reason in result.reasons:
            print(f"  - {reason}")
        raise SystemExit(0)

    print("MISS")
    for reason in result.reasons:
        print(f"  - {reason}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
