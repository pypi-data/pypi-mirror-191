# -*- coding=utf-8 -*-

"""Attributes container class module."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Iterator

from revsymg.exceptions import WrongAttributeType, _NoAttribute, _NoKey
from revsymg.lib.index_lib import IndexT


# ============================================================================ #
#                           ATTRIBUTES CONCRETE CLASS                          #
# ============================================================================ #
class AttributesContainer():
    """Attributes container class."""

    def __init__(self):
        """The Initializer."""
        self._card_keys: int = 0
        self._attrname_index_default: dict[str, tuple[IndexT, Any]] = {}
        self._lists_values: list[list[Any]] = []

    def card_properties(self) -> int:
        """Return the number of attributes fields.

        Returns
        -------
        int
            Number of attributes fields
        """
        return len(self._lists_values)

    def names(self) -> Iterable[str]:
        """Return the attributes name.

        Returns
        -------
        iterable of str
            Attributes names
        """
        return self._attrname_index_default

    def has_attrname(self, attrname: str) -> bool:
        """Return True if there is a property named attrname.

        Parameters
        ----------
        attrname : str
            Property's name

        Returns
        -------
        bool
            Is attrname in property names?
        """
        return attrname in self._attrname_index_default

    def get(self, key: IndexT, attrname: str) -> Any:
        """Return the value associated to the `key` attribute `attrname`.

        Parameters
        ----------
        key : IndexT
            Object index
        attrname : str
            Attribute name

        Returns
        -------
        Any
            Attribute value

        Raises
        ------
        _NoAttribute
            No attribute
        _NoKey
            Key does not exist
        """
        try:
            attr_index, _ = self._attrname_index_default[attrname]
        except KeyError as key_error:
            raise _NoAttribute(attrname) from key_error
        try:
            return self._lists_values[attr_index][key]
        except IndexError as index_error:
            raise _NoKey(key) from index_error

    def get_all(self, key: IndexT) -> Iterator[tuple[str, Any]]:
        """Iterate over attribute name and values for the key.

        Parameters
        ----------
        key : IndexT
            Object index

        Yields
        ------
        str, Any
            Attribute name, and all values

        Raises
        ------
        _NoKey
            Key does not exist
        """
        if key >= self._card_keys:
            raise _NoKey(key)
        for attrname, (attr_index, _) in self._attrname_index_default.items():
            yield attrname, self._lists_values[attr_index][key]

    def new_attr(self, attrname: str, default: Any):
        """Add an attribute entry.

        Parameters
        ----------
        attrname : str
            Attribute's name
        default : Any
            Default keys' attribute value
        """
        if attrname in self._attrname_index_default:
            attr_index, _ = self._attrname_index_default[attrname]
        else:
            attr_index = len(self._attrname_index_default)
            self._lists_values.append([])
        self._attrname_index_default[attrname] = (attr_index, default)
        self._lists_values[attr_index] = [default] * self._card_keys

    def add_keys(self, number: int = 1):
        """Add number of keys.

        Parameters
        ----------
        number : int, default 1
            Number of keys to add
        """
        self._card_keys += number
        for attr_index, default in self._attrname_index_default.values():
            self._lists_values[attr_index] += [default] * number

    def set_attr(self, key: IndexT, attrname: str, attrvalue: Any):
        """Set the values for the attributes, else create them.

        Parameters
        ----------
        key : IndexT
            Object index
        attrname : str
            Attribute's name
        attrvalue : Any
            Attribute's value

        Raises
        ------
        _NoAttribute
            There is one attribute's name that was not added before
        WrongAttributeType
            Given value does not correspond to attribute's type
        _NoKey
            Key does not exist
        """
        try:
            attr_index, default = self._attrname_index_default[attrname]
        except KeyError as key_error:
            raise _NoAttribute(attrname) from key_error
        if not isinstance(attrvalue, type(default)):
            raise WrongAttributeType(attrvalue, type(default))
        try:
            self._lists_values[attr_index][key] = attrvalue
        except IndexError as index_error:
            raise _NoKey(key) from index_error

    def delete_key(self, key: IndexT):
        """Delete an entire key.

        Parameters
        ----------
        key : IndexT
            Key to delete

        Raises
        ------
        _NoKey
            Key does not exist

        Warning
        -------
        This operation may invalidate keys' index. In fact, deleting one key
        implies shifting all next indices. Because of this, keys should always
        be removed in decreasing index order:

        >>> for key in sorted(keys_to_del, reverse=True):
        >>>     attr_container.delete_key(key)
        """
        if key >= self._card_keys:
            raise _NoKey(key)
        for attr_index, values in enumerate(self._lists_values):
            self._lists_values[attr_index] = values[:key] + values[key + 1:]
        self._card_keys -= 1

    def delete_keys(self, keys: Iterable[IndexT]):
        """Delete entire keys.

        Parameters
        ----------
        keys : iterable of IndexT
            Keys to delete

        Raises
        ------
        _NoKey
            Key does not exist

        Note
        ----
        At the oposite of :meth:`~revsymg.AttributesContainer.delete_key`
        method, it is not necessary to sort `keys`. This is done internally.
        """
        for key in sorted(keys, reverse=True):
            if key >= self._card_keys:
                raise _NoKey(key)
            for attr_index, values in enumerate(self._lists_values):
                self._lists_values[attr_index] = values[:key] + values[key + 1:]
            self._card_keys -= 1
