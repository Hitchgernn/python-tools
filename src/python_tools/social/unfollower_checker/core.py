"""Simple unfollower checker from two username lists."""

from __future__ import annotations

from pathlib import Path


def _load_usernames(path: str) -> set[str]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip()}


def find_unfollowers(following_path: str, followers_path: str) -> list[str]:
    following = _load_usernames(following_path)
    followers = _load_usernames(followers_path)
    return sorted(following - followers)
