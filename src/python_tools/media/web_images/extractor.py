"""Extract image links from a web page."""

from __future__ import annotations

import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from python_tools.common.http import build_session


CSS_URL_RE = re.compile(r"url\((['\"]?)(.*?)\1\)")


def _split_srcset(value: str) -> list[str]:
    urls: list[str] = []
    for item in value.split(","):
        part = item.strip().split(" ")[0]
        if part:
            urls.append(part)
    return urls


def extract_image_urls(page_url: str) -> list[str]:
    session = build_session()
    response = session.get(page_url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    found: set[str] = set()

    for img in soup.select("img[src]"):
        found.add(urljoin(page_url, img["src"]))

    for source in soup.select("source[srcset]"):
        for candidate in _split_srcset(source["srcset"]):
            found.add(urljoin(page_url, candidate))

    for node in soup.select("[style]"):
        for _, candidate in CSS_URL_RE.findall(node.get("style", "")):
            if candidate:
                found.add(urljoin(page_url, candidate))

    return sorted(found)
