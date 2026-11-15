"""Print open incidents from incidents.csv."""

import argparse
import csv
import sys


def load(path: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return [row for row in csv.DictReader(handle) if row["status"] == "open"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="incidents.csv")
    args = parser.parse_args(argv)
    for row in load(args.path):
        print(f"{row['id']}\t{row['severity']}\t{row['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
