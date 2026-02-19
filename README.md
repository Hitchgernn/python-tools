# python-tools

A modular Python toolkit for media and social utilities.

This repo includes:
- YouTube downloader (audio/video)
- TikTok downloader (audio/video)
- Web image URL extractor
- Unfollower checker (from two username lists)

## Requirements

- Python `3.10+`
- `ffmpeg` (required for audio extraction/merging in `yt-dlp` workflows)

Install `ffmpeg`:

```bash
# Fedora
sudo dnf install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg
```

## Installation

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
```

This installs command entrypoints defined in `pyproject.toml`.

## Quick Start

```bash
python-tools --help
```

Main command groups:
- `yt`
- `tiktok`
- `web-images`
- `unfollowers`

## Command Usage

### 1) YouTube downloader

Download audio (default mode):

```bash
python-tools yt "https://youtube.com/watch?v=VIDEO_ID"
```

Download video:

```bash
python-tools yt "https://youtube.com/watch?v=VIDEO_ID" --mode video
```

Custom filename (without extension):

```bash
python-tools yt "https://youtube.com/watch?v=VIDEO_ID" --mode audio --output "my_track"
```

### 2) TikTok downloader

Download audio:

```bash
python-tools tiktok "https://www.tiktok.com/@user/video/123" --mode audio
```

Download video:

```bash
python-tools tiktok "https://www.tiktok.com/@user/video/123" --mode video
```

Notes:
- TikTok `/photo/` posts are unreliable for video downloads.
- The audio path attempts a `/photo/ -> /video/` fallback.

### 3) Web image extractor

Extract image URLs from a page:

```bash
python-tools web-images "https://example.com"
```

Write output to a custom file:

```bash
python-tools web-images "https://example.com" --output data/reports/images.txt
```

### 4) Unfollower checker

Given two text files (one username per line):
- `following.txt`
- `followers.txt`

Run:

```bash
python-tools unfollowers --following following.txt --followers followers.txt
```

Custom output file:

```bash
python-tools unfollowers --following following.txt --followers followers.txt --output data/reports/unfollowers.txt
```

## Alternate script wrappers

You can also run thin wrappers in `tools/`:

```bash
python tools/yt.py "https://youtube.com/watch?v=VIDEO_ID" -m audio
python tools/tiktok.py "https://www.tiktok.com/@user/video/123" -m video
python tools/web_images.py "https://example.com"
python tools/unfollowers.py --following following.txt --followers followers.txt
```

## Output Locations

By default, outputs are written under `data/`:
- Downloads: `data/downloads/`
- Reports: `data/reports/`
- Images directory placeholder: `data/images/`

Change output root with env var:

```bash
export PYTHON_TOOLS_DATA_DIR=/path/to/output-root
```

## Project Structure

```text
python-tools/
├─ README.md
├─ pyproject.toml
├─ .gitignore
├─ .env.example
├─ src/
│  └─ python_tools/
│     ├─ cli.py
│     ├─ common/
│     ├─ media/
│     └─ social/
├─ tools/
├─ tests/
└─ data/
```

## Development

Run tests (if installed):

```bash
python -m pytest -q
```

If pytest is missing:

```bash
python -m pip install pytest
```

## Troubleshooting

- `ffmpeg not found`: install `ffmpeg` and ensure it is in `PATH`.
- Download failures: update dependencies:
  ```bash
  python -m pip install -U yt-dlp
  ```
- Some sites require cookies/session context; behavior depends on platform restrictions.
