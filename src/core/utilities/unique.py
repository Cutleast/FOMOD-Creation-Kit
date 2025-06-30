"""
Copyright (c) Cutleast
"""

from typing import Any, Callable, Iterable, Optional


def unique[T](
    iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None
) -> list[T]:
    """
    Removes all duplicates from an iterable.

    Args:
        iterable (Iterable[T]): Iterable with duplicates.
        key (Optional[Callable[[T], Any]], optional):
            Key function to identify unique elements. Defaults to None.

    Returns:
        list[T]: List without duplicates.
    """

    if key is None:
        # in contrast to list(set(iterable)) this will preserve the order
        return list({item: None for item in iterable}.keys())

    else:
        return list({key(item): item for item in iterable}.values())
