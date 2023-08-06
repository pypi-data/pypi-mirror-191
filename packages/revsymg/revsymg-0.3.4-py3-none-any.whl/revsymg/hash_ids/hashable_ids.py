# -*- coding=utf-8 -*-

"""Hashable reads' identifiers container class module."""

from __future__ import annotations

from collections.abc import Hashable
from typing import Generator

from revsymg.exceptions import NoReadId, NoVertexIndex
from revsymg.hash_ids.abstract_ids import AbstractIdsContainer
from revsymg.lib.index_lib import FORWARD_INT, IND, IndexT, IndOrT, OrT


# ============================================================================ #
#                          HASHABLE READS IDENTIFIERS                          #
# ============================================================================ #
class HashableIdsContainer(AbstractIdsContainer[Hashable]):
    """Reads identifier container for hashable identifiers."""

    def __init__(self):
        """The initializer."""
        # List vertex index to vertex id
        #   [v.index]: v.idr
        self._indices_ids: list[Hashable] = []
        # dictionary vertex id to vertex index
        #   v.idr -> v.index
        self._ids_indices: dict[Hashable, IndexT] = {}

    # -*- Identifier -*-

    def id_to_indor(self, read_id: Hashable,
                    orientation: OrT = FORWARD_INT) -> IndOrT:
        """Return the oriented vertex associated to the id.

        Parameters
        ----------
        read_id : Hashable
            Read's identifier
        orientation : OrT, default FORWARD_INT
            Read orientation

        Returns
        -------
        IndOrT
            Oriented vertex

        Raises
        ------
        NoReadId
            If there is no read's identifier in container
        """
        try:
            return self._ids_indices[read_id], orientation
        except KeyError as exc:
            raise NoReadId(read_id) from exc

    def indor_to_id(self, vertex: IndOrT) -> Hashable:
        """Return the id from vertices.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Returns
        -------
        Hashable
            The associated read's identifier

        Raises
        ------
        NoVertexIndex
            There is no read's identifier corresponding to given vertex
        """
        try:
            return self._indices_ids[vertex[IND]]
        except IndexError as exc:
            raise NoVertexIndex(vertex[IND]) from exc

    # -*- Setter -*-

    def add(self, read_id: Hashable) -> IndexT:
        """Add an entry if identifier not yet recorded else corresponding index.

        Parameters
        ----------
        read_id : Hasable
            Read's identifier

        Returns
        -------
        IndexT
            Associated vertex index
        """
        try:
            return self._ids_indices[read_id]
        except KeyError:
            self._ids_indices[read_id] = len(self._indices_ids)
            self._indices_ids.append(read_id)
        return self._ids_indices[read_id]

    def pop(self, read_id: Hashable) -> IndexT:
        """Remove read's identifier.

        Parameters
        ----------
        read_id : Hashable
            Read's identifier

        Returns
        -------
        IndexT
            Index corresponding to read's identifier

        Raises
        ------
        NoReadId
            If there is no read's identifier in container
        """
        try:
            index = self._ids_indices.pop(read_id)
        except KeyError as exc:
            raise NoReadId(read_id) from exc
        self._indices_ids = (
            self._indices_ids[:index] + self._indices_ids[index + 1:]
        )
        for post_id in self._indices_ids[index:]:
            self._ids_indices[post_id] -= 1
        return index

    # -*- Overloaded built-in -*-

    def __iter__(self) -> Generator[Hashable, None, None]:
        """Iterate on reads' identifier.

        Yields
        ------
        Hashable
            Reads' identifier
        """
        yield from self._ids_indices.keys()

    def __contains__(self, read_id: Hashable) -> bool:
        """Return True if read's identifier in container.

        Parameters
        ----------
        read_id : Hashable
            Read's identifier

        Returns
        -------
        bool
            Is read's identifier in container?
        """
        return read_id in self._ids_indices

    def __len__(self) -> int:
        """Return the number of recorded read's identifiers.

        Returns
        -------
        int
            Number of reads' identifiers
        """
        return len(self._indices_ids)
