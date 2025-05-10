"""
Copyright (c) Cutleast
"""

from enum import Enum


class Order(Enum):
    """
    Enum for the possible orders of items.
    """

    Ascending = "Ascending"
    """Indicates the items are to be ordered ascending alphabetically."""

    Descending = "Descending"
    """Indicates the items are to be ordered descending alphabetically."""

    Explicit = "Explicit"
    """Indicates the items are to be ordered as listed in the configuration file."""
