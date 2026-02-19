"""Unified CLI for python_tools."""

import argparse

from python_tools.media.tiktok_downloader.cli import add_parser as add_tiktok_parser
from python_tools.media.web_images.cli import add_parser as add_web_images_parser
from python_tools.media.yt_downloader.cli import add_parser as add_yt_parser
from python_tools.social.unfollower_checker.cli import add_parser as add_unfollowers_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python-tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_yt_parser(subparsers)
    add_tiktok_parser(subparsers)
    add_web_images_parser(subparsers)
    add_unfollowers_parser(subparsers)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
