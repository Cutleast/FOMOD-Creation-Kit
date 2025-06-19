"""
Copyright (c) Cutleast
"""

import traceback
from abc import abstractmethod
from typing import Any


def format_exception(
    exception: BaseException, only_message_when_localized: bool = True
) -> str:
    """
    Formats an exception to a string.

    Args:
        exception (BaseException): The exception to format.
        only_message_when_localized (bool):
            Whether to only return the message when localized.

    Returns:
        str: Formatted exception
    """

    if isinstance(exception, ExceptionBase) and only_message_when_localized:
        return str(exception)

    return "".join(traceback.format_exception(exception))


class ExceptionBase(Exception):
    """
    Base Exception class for localized exceptions.
    """

    def __init__(self, *values: Any) -> None:
        super().__init__(self._get_localized_message().format(*values))

    @abstractmethod
    def _get_localized_message(self) -> str:
        """
        Returns raw localized message with placeholders. Use `__str__()` to get the full
        message.

        Returns:
            str: Localized message with placeholders
        """
