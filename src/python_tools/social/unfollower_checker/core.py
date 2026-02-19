"""Unfollower checker from text or JSON username sources."""

from __future__ import annotations

import json
from pathlib import Path


USERNAME_KEYS = {"value", "username", "user", "handle"}


def _extract_instagram_usernames(payload: object, key_hint: str | None = None) -> set[str]:
    usernames: set[str] = set()

    if isinstance(payload, dict):
        for key, value in payload.items():
            usernames.update(_extract_instagram_usernames(value, key))
        return usernames

    if isinstance(payload, list):
        for item in payload:
            usernames.update(_extract_instagram_usernames(item, key_hint))
        return usernames

    if isinstance(payload, str):
        username = payload.strip()
        if username and (key_hint in USERNAME_KEYS or key_hint is None):
            usernames.add(username)
        return usernames

    return usernames


def _extract_from_instagram_item(item: dict) -> str | None:
    string_list_data = item.get("string_list_data")
    if not isinstance(string_list_data, list) or not string_list_data:
        return None
    first = string_list_data[0]
    if not isinstance(first, dict):
        return None
    value = first.get("value")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _extract_usernames_from_json(path: Path) -> set[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))

    # Instagram exports usually store usernames in objects like:
    # {"string_list_data":[{"value":"username", ...}]}
    usernames: set[str] = set()
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                username = _extract_from_instagram_item(item)
                if username:
                    usernames.add(username)
    elif isinstance(payload, dict):
        usernames.update(_extract_instagram_usernames(payload))

        for value in payload.values():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        username = _extract_from_instagram_item(item)
                        if username:
                            usernames.add(username)

    return usernames


def _load_usernames(path: str) -> set[str]:
    source = Path(path)
    if source.suffix.lower() == ".json":
        return _extract_usernames_from_json(source)

    lines = source.read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip()}


def find_unfollowers(following_path: str, followers_path: str) -> list[str]:
    following = _load_usernames(following_path)
    followers = _load_usernames(followers_path)
    return sorted(following - followers)
