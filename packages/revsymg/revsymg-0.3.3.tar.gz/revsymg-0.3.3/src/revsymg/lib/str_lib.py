# -*- coding=utf-8 -*-

"""Library for reads."""

from __future__ import annotations

from typing import TypeVar


# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
IdT = TypeVar('IdT')
"""Identifier type."""


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                              Reads Orientations                              #
# ---------------------------------------------------------------------------- #
FORWARD_STR: str = '_f'
"""Forward string representation."""

REVERSE_STR: str = '_r'
"""Reverse string representation."""

STRAND_STR = (
    FORWARD_STR,
    REVERSE_STR,
)
"""Orientation binary value to string value."""
