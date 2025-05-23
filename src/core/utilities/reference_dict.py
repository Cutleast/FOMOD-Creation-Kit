"""
Copyright (c) Cutleast
"""

from typing import Iterable


class ReferenceDict[K, V]:
    """
    Dict-like container with reference keys. Useful for mutable objects that
    can be altered without destroying the mapping to the value.

    Also doesn't require hashable keys.
    """

    __values: dict[int, tuple[K, V]]

    def __init__(self, initial: dict[K, V] = {}) -> None:
        self.__values = {id(k): (k, v) for k, v in initial.items()}

    def __getitem__(self, key: K) -> V:
        return self.__values[id(key)][1]

    def __setitem__(self, key: K, value: V) -> None:
        self.__values[id(key)] = key, value

    def __delitem__(self, key: K) -> None:
        del self.__values[id(key)]

    def __contains__(self, key: K) -> bool:
        return id(key) in self.__values

    def __len__(self) -> int:
        return len(self.__values)

    def keys(self) -> Iterable[K]:
        for item in self.__values.values():
            yield item[0]

    def values(self) -> Iterable[V]:
        for item in self.__values.values():
            yield item[1]

    def items(self) -> Iterable[tuple[K, V]]:
        return self.__values.values()

    def pop(self, key: K) -> V:
        return self.__values.pop(id(key))[1]

    def clear(self) -> None:
        self.__values.clear()
