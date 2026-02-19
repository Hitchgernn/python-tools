"""Core TikTok download logic via yt-dlp."""

from __future__ import annotations

from python_tools.media.yt_downloader.core import clean_url, download_audio as yt_download_audio
from python_tools.media.yt_downloader.core import download_video as yt_download_video


def _is_photo_mode(url: str) -> bool:
    return "tiktok.com" in url and "/photo/" in url


def _convert_photo_to_video_url(url: str) -> str:
    return url.replace("/photo/", "/video/")


def download_audio(url: str, output_name: str | None = None) -> None:
    normalized = clean_url(url)
    if _is_photo_mode(normalized):
        normalized = _convert_photo_to_video_url(normalized)
    yt_download_audio(normalized, output_name)


def download_video(url: str, output_name: str | None = None) -> None:
    normalized = clean_url(url)
    if _is_photo_mode(normalized):
        raise ValueError("TikTok /photo/ posts are not reliably downloadable as video.")
    yt_download_video(normalized, output_name)
