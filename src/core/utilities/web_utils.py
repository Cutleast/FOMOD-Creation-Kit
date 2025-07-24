"""
Copyright (c) Cutleast
"""

import logging
from typing import Optional

from requests import Response, get

from .cache import cache

log: logging.Logger = logging.getLogger("WebUtils")


@cache
def get_raw_web_content(url: str) -> Optional[bytes]:
    """
    Fetches raw content from the given URL. The result is cached.

    Args:
        url (str): URL to fetch content from.

    Returns:
        Optional[bytes]: Raw content of the URL or `None` if the request failed.
    """

    res: Response = get(url)

    if res.status_code == 200:
        return res.content

    log.error(f"Failed to fetch content from '{url}'. Status Code: {res.status_code}")
