"""CLI for web image extraction."""

from __future__ import annotations

import argparse
from pathlib import Path

from python_tools.common.fs import ensure_output_dir
from python_tools.media.web_images.extractor import extract_image_urls


def _run(args: argparse.Namespace) -> int:
    urls = extract_image_urls(args.url)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_path = ensure_output_dir("reports") / "web_images.txt"
    out_path.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"Wrote {len(urls)} image URLs to {out_path}")
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("web-images", help="Extract image URLs from a page")
    parser.add_argument("url", help="Page URL")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.set_defaults(func=_run)


def main() -> int:
    parser = argparse.ArgumentParser(prog="web-images")
    parser.add_argument("url", help="Page URL")
    parser.add_argument("-o", "--output", help="Output file path")
    return _run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
