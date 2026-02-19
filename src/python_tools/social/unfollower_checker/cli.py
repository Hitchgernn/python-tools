"""CLI for unfollower checker."""

from __future__ import annotations

import argparse
from pathlib import Path

from python_tools.common.fs import ensure_output_dir
from python_tools.social.unfollower_checker.core import find_unfollowers


def _run(args: argparse.Namespace) -> int:
    users = find_unfollowers(args.following, args.followers)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_path = ensure_output_dir("reports") / "unfollowers.txt"
    out_path.write_text("\n".join(users) + "\n", encoding="utf-8")
    print(f"Wrote {len(users)} users to {out_path}")
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("unfollowers", help="Compare following vs followers lists")
    parser.add_argument("--following", required=True, help="Path to following usernames (one per line)")
    parser.add_argument("--followers", required=True, help="Path to follower usernames (one per line)")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.set_defaults(func=_run)


def main() -> int:
    parser = argparse.ArgumentParser(prog="unfollowers")
    parser.add_argument("--following", required=True, help="Path to following usernames (one per line)")
    parser.add_argument("--followers", required=True, help="Path to follower usernames (one per line)")
    parser.add_argument("-o", "--output", help="Output file path")
    return _run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
