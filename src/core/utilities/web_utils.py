"""
Copyright (c) Cutleast
"""

from requests import get

from .cache import cache


@cache
def get_raw_web_content(url: str) -> bytes:
    """
    Fetches raw content from the given URL. The result is cached.

    Args:
        url (str): URL to fetch content from.

    Returns:
        bytes: Raw content of the URL.
    """

    return get(url).content
