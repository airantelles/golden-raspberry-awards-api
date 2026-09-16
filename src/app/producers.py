"""Parsing of producer lists from the CSV dataset."""

import re

_SEPARATOR = re.compile(r"\s*,\s*(?:and\s+)?|\s+and\s+")


def parse_producers(value: str) -> list[str]:
    """Split the producer-list formats used by the dataset.

    Commas and the standalone conjunction ``and`` are separators. Whitespace in
    names is reduced to a single space so that incidental spacing does not
    create distinct producers.
    """
    names = [" ".join(name.split()) for name in _SEPARATOR.split(value)]
    if not all(names):
        raise ValueError("invalid producers list")
    return list(dict.fromkeys(names))
