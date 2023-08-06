# -*- coding=utf-8 -*-

"""0-based indices reads' identifiers container class module."""

from __future__ import annotations

from typing import Generator, Optional, cast

from revsymg.exceptions import NoReadId, NoVertexIndex
from revsymg.hash_ids.abstract_ids import AbstractIdsContainer
from revsymg.hash_ids.hashable_ids import HashableIdsContainer
from revsymg.lib.index_lib import FORWARD_INT, IND, IndexT, IndOrT, OrT


# ============================================================================ #
#                       INDICES 0 BASED READS IDENTIFIERS                      #
# ============================================================================ #
class IndicesIdsContainer(AbstractIdsContainer[IndexT]):
    """Reads identifier container for 0-based indentifiers."""

    def __init__(self):
        """The Initializer."""
        # Valid until the 0-based index property becomes false
        self._card_id: int = 0
        # Valid when the 0-based index property becomes false
        self._readsid_container: Optional[HashableIdsContainer] = None

    # -*- Identifiers -*-

    def id_to_indor(self, read_id: IndexT,
                    orientation: OrT = FORWARD_INT) -> IndOrT:
        """Return the oriented vertex associated to the id.

        Parameters
        ----------
        read_id : IdT
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
        if self._readsid_container is None:
            if read_id < self._card_id:
                return read_id, orientation
            raise NoReadId(read_id)
        return self._readsid_container.id_to_indor(read_id, orientation)

    def indor_to_id(self, vertex: IndOrT) -> IndexT:
        """Return the id from vertices.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Returns
        -------
        IndexT
            The associated read's identifier

        Raises
        ------
        NoVertexIndex
            There is no read's identifier corresponding to given vertex
        """
        if self._readsid_container is None:
            if vertex[IND] >= self._card_id:
                raise NoVertexIndex(vertex[IND])
            return vertex[IND]
        return cast(IndexT, self._readsid_container.indor_to_id(vertex))

    # -*- Setter -*-

    def add(self, read_id: IndexT) -> IndexT:
        r"""Add an entry if identifier not yet recorded.

        Parameters
        ----------
        read_id : IndexT
            Read's identifier

        Returns
        -------
        IndexT
            Associated vertex index

        Notes
        -----
        It considers bijective-property respected (read's identifiers are
        0-base indices), thus it adds all read's identifiers between the
        :math:`max(r_{id} \in \mathcal{R_{id}}` and new :math:`r_{id}`

        If the property was violated, only new :math:`r_{id}` is added.
        """
        if self._readsid_container is None:
            if read_id < self._card_id:
                return read_id
            self._card_id += 1
            return self._card_id - 1
        return self._readsid_container.add(read_id)

    def pop(self, read_id: IndexT) -> IndexT:
        """Remove read's identifier.

        Parameters
        ----------
        read_id : int
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
        if self._readsid_container is None:
            if read_id > self._card_id - 1:
                raise NoReadId(read_id)
            if read_id == self._card_id - 1:  # property not yet violated
                self._card_id -= 1
            elif read_id < self._card_id - 1:  # property violated
                self._readsid_container = HashableIdsContainer()
                for r_id in range(self._card_id):
                    if r_id != read_id:
                        self._readsid_container.add(r_id)
            return read_id
        return self._readsid_container.pop(read_id)

    # -*- Overloaded built-in -*-

    def __iter__(self) -> Generator[IndexT, None, None]:
        """Iterate on reads' identifier.

        Yields
        ------
        IndexT
            Reads' identifier
        """
        if self._readsid_container is None:
            yield from range(self._card_id)
        else:
            yield from (
                cast(IndexT, read_id) for read_id in self._readsid_container
            )

    def __contains__(self, read_id: IndexT) -> bool:
        """Return True if read's identifier in container.

        Parameters
        ----------
        read_id : IndexT
            Read's identifier

        Returns
        -------
        bool
            Is read's identifier in container?
        """
        if self._readsid_container is None:
            return read_id < self._card_id
        return read_id in self._readsid_container

    def __len__(self) -> int:
        """Return the number of recorded read's identifiers.

        Returns
        -------
        int
            Number of reads' identifiers
        """
        if self._readsid_container is None:
            return self._card_id
        return len(self._readsid_container)
