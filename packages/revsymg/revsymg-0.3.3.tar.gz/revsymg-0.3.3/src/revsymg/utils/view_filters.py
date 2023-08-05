# -*- coding=utf-8 -*-

"""Filters utility module."""

from collections.abc import Callable, Hashable
from typing import Any


FilterT = Callable[..., bool]


def always_true(*args: tuple[Any, ...],  # pylint: disable=unused-argument
                **kwargs: dict[Hashable, Any]) -> bool:
    """Return always True value.

    Parameters
    ----------
    args : Any
        Anything
    kwargs : Any
        Anything

    Returns
    -------
    bool
        True
    """
    return True
