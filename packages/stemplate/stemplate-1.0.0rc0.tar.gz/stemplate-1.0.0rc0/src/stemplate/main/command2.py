# -*- coding: utf-8 -*-

"""Command2 module.

This module implements the functionality that allows...
"""

from datetime import datetime, timezone

PARAMETERS = {}

def main(**kwargs) -> None:
    """Print the date."""
    date = datetime.now(timezone.utc)
    zone = date.astimezone().tzinfo
    str1 = date.isoformat(timespec="seconds")
    str2 = date.astimezone(zone).isoformat(timespec="seconds")
    print(f"{str1} (UTC)")
    print(f"{str2} ({zone})")
