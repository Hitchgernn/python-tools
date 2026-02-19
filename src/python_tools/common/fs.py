"""Filesystem helpers."""

from __future__ import annotations

import os
import re
from pathlib import Path


INVALID_FILENAME_CHARS = r'[\\/:*?"<>|]+'


def sanitize_filename(name: str) -> str:
    name = name.strip()
    if not name:
        return ""
    name = re.sub(INVALID_FILENAME_CHARS, "_", name)
    return re.sub(r"\s+", " ", name).strip()


def ensure_output_dir(*parts: str) -> Path:
    base = Path(os.environ.get("PYTHON_TOOLS_DATA_DIR", "data"))
    out = base.joinpath(*parts)
    out.mkdir(parents=True, exist_ok=True)
    return out
