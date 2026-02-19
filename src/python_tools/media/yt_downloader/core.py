"""Core YouTube download logic via yt-dlp."""

from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

import yt_dlp

from python_tools.common.fs import ensure_output_dir


def clean_url(url: str) -> str:
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _progress_hook(payload: dict) -> None:
    if payload.get("status") == "finished":
        print("\nDone downloading, starting post-processing...")


def _detect_browser_for_cookies() -> str | None:
    candidates = ["firefox", "chrome", "chromium", "brave", "edge", "opera", "vivaldi"]
    for browser in candidates:
        try:
            yt_dlp.cookies.extract_cookies_from_browser(browser)
            return browser
        except Exception:
            continue
    return None


def _get_impersonate_target():
    try:
        from yt_dlp.networking.impersonate import ImpersonateTarget

        return ImpersonateTarget.from_str("chrome")
    except Exception:
        return None


def download_audio(url: str, output_name: str | None = None) -> None:
    url = clean_url(url)
    outdir = ensure_output_dir("downloads", "youtube")
    browser = _detect_browser_for_cookies()
    impersonate_target = _get_impersonate_target()
    outtmpl = str(outdir / (f"{output_name}.%(ext)s" if output_name else "%(title)s.%(ext)s"))

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "progress_hooks": [_progress_hook],
        "quiet": False,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ],
        **({"cookiesfrombrowser": (browser,)} if browser else {}),
        **({"impersonate": impersonate_target} if impersonate_target else {}),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_video(url: str, output_name: str | None = None) -> None:
    url = clean_url(url)
    outdir = ensure_output_dir("downloads", "youtube")
    browser = _detect_browser_for_cookies()
    impersonate_target = _get_impersonate_target()
    outtmpl = str(outdir / (f"{output_name}.%(ext)s" if output_name else "%(title)s.%(ext)s"))

    ydl_opts = {
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "progress_hooks": [_progress_hook],
        "quiet": False,
        **({"cookiesfrombrowser": (browser,)} if browser else {}),
        **({"impersonate": impersonate_target} if impersonate_target else {}),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
