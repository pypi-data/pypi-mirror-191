# -*- coding=utf-8 -*-

"""Reads' identifiers container abstract base class module."""

from __future__ import annotations

from abc import abstractmethod
from typing import Generator, Generic

from revsymg.lib.index_lib import FORWARD_INT, IndexT, IndOrT, OrT
from revsymg.lib.str_lib import IdT


# ============================================================================ #
#                     READS IDENTIFIERS CONTAINER ABSTRACT                     #
# ============================================================================ #
class AbstractIdsContainer(Generic[IdT]):
    """Abstract class for reads identifiers container."""

    # -*- Identifiers -*-

    # pylint: disable=missing-param-doc
    @abstractmethod
    def id_to_indor(self, read_id: IdT,
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
        raise NotImplementedError

    @abstractmethod
    def indor_to_id(self, vertex: IndOrT) -> IdT:
        """Return the id from vertices.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Returns
        -------
        IdT
            The associated read's identifier

        Raises
        ------
        NoVertex
            There is no read's identifier corresponding to given vertex
        """
        raise NotImplementedError

    # -*- Setter -*-

    @abstractmethod
    def add(self, read_id: IdT) -> IndexT:
        """Add an entry if identifier not yet recorded else corresponding index.

        Parameters
        ----------
        read_id : IdT
            Read's identifier

        Returns
        -------
        IndexT
            Associated vertex index
        """
        raise NotImplementedError

    @abstractmethod
    def pop(self, read_id: IdT) -> IndexT:
        """Remove read's identifier.

        Parameters
        ----------
        read_id : IdT
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
        raise NotImplementedError

    # -*- Overloaded built-in -*-

    # DOC: special method

    @abstractmethod
    def __iter__(self) -> Generator[IdT, None, None]:
        """Iterate on reads' identifier.

        Yields
        ------
        IdT
            Reads' identifier
        """
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, read_id: IdT) -> bool:
        """Return True if read's identifier in container.

        Parameters
        ----------
        read_id : IdT
            Read's identifier

        Returns
        -------
        bool
            Is read's identifier in container?
        """
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of recorded read's identifiers.

        Returns
        -------
        int
            Number of reads' identifiers
        """
        raise NotImplementedError
