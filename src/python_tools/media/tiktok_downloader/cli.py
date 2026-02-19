"""CLI for TikTok downloader."""

from __future__ import annotations

import argparse

from python_tools.common.fs import sanitize_filename
from python_tools.media.tiktok_downloader.core import download_audio, download_video


def _run(args: argparse.Namespace) -> int:
    output_name = sanitize_filename(args.output) if args.output else None
    if args.mode == "audio":
        download_audio(args.url, output_name)
    else:
        download_video(args.url, output_name)
    return 0


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("tiktok", help="Download from TikTok")
    parser.add_argument("url", help="TikTok URL")
    parser.add_argument("-m", "--mode", choices=["audio", "video"], default="audio")
    parser.add_argument("-o", "--output", help="Optional output filename (without extension)")
    parser.set_defaults(func=_run)


def main() -> int:
    parser = argparse.ArgumentParser(prog="tiktok")
    parser.add_argument("url", help="TikTok URL")
    parser.add_argument("-m", "--mode", choices=["audio", "video"], default="audio")
    parser.add_argument("-o", "--output", help="Optional output filename (without extension)")
    return _run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
