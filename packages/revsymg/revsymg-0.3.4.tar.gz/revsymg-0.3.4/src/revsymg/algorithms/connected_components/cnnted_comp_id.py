# -*- coding=utf-8 -*-

"""Connected component identifiers containers classes module."""

from __future__ import annotations

from typing import Iterator, Optional

from revsymg.exceptions import NoConnectedComponentId, NoVertexIndex
from revsymg.lib.index_lib import (
    FORWARD_INT,
    FWDOR_REVOR,
    IND,
    OR,
    ORIENT_REV,
    REVERSE_INT,
    IndexT,
    IndOrT,
    OrT,
)


# ============================================================================ #
#                     REVERSE SYMMETRIC CONNECTED COMPONENT                    #
# ============================================================================ #
class _RevSymCCIdFactory():
    """Connected component identifiers container builder.

    Warnings
    --------
    You must not use this class.
    """

    def __init__(self, card_index: int):
        """The Initializer."""
        # Number of disctint connected components
        self._nb_distinct: int = 0
        # Current couple of connected component identifiers
        self._ccompids_cur: tuple[IndexT, IndexT] = (0, 1)
        # Index of current couple of connected component identifier
        self._ccompid_ind: IndexT = -1
        # List of couples of connected component identifiers
        self._cc_couples: list[tuple[IndexT, IndexT]] = []
        # List of forward vertices connected component identifier
        self._f_vertices_cc: list[Optional[tuple[IndexT, OrT]]] = [
            None for _ in range(card_index)
        ]

    def new_cc_couple(self):
        """Set the couple of connected component Ids."""
        self._ccompid_ind += 1
        self._ccompids_cur = (
            self._nb_distinct, self._nb_distinct + 1,
        )
        self._cc_couples.append(self._ccompids_cur)
        self._nb_distinct += 2

    def set_cc_id(self, vertex: IndOrT):
        """Set the connected component identifiers to `vertex` and its reverse.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            self._f_vertices_cc[vertex[IND]] = (self._ccompid_ind, vertex[OR])
        except IndexError as index_err:
            raise NoVertexIndex(vertex[IND]) from index_err

    def continuity(self, vertex: IndOrT) -> bool:
        """Return True if the continuity is respected.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Returns
        -------
        bool
            True if both strands are not in the same connected component

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        NoConnectedComponentId
            If vertex is not associated with any connected component
        """
        try:
            cc_indor = self._f_vertices_cc[vertex[IND]]
        except IndexError as index_err:
            raise NoVertexIndex(vertex[IND]) from index_err
        if cc_indor is None:
            raise NoConnectedComponentId(vertex)
        return (
            self._cc_couples[cc_indor[IND]][
                FWDOR_REVOR[vertex[OR]][cc_indor[OR]]
            ]
            == self._ccompids_cur[FORWARD_INT]
        )

    def merge_cc(self):
        """In case the two strands are confused, the ccomp ids are the equal."""
        self._nb_distinct -= 1
        self._ccompids_cur = (
            self._ccompids_cur[FORWARD_INT],
            self._ccompids_cur[FORWARD_INT],
        )
        self._cc_couples[self._ccompid_ind] = self._ccompids_cur

    def to_readonly_view(self) -> RevSymCCId:
        """Return a read-only view.

        Returns
        -------
        RevSymCCId
            Connected component identifier container
        """
        return RevSymCCId(
            self._nb_distinct, self._cc_couples, self._f_vertices_cc,
        )

    def __getitem__(self, vertex: IndOrT) -> Optional[IndexT]:
        """Return the cc number of oriented vertex.

        Parameters
        ----------
        vertex : IndOrT
            oriented vertex

        Returns
        -------
        IndexT or None
            Connected component identifier if exist or None

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            cc_indor = self._f_vertices_cc[vertex[IND]]
        except IndexError as index_err:
            raise NoVertexIndex(vertex[IND]) from index_err
        if cc_indor is not None:
            return self._cc_couples[cc_indor[IND]][
                FWDOR_REVOR[vertex[OR]][cc_indor[OR]]
            ]
        return None


class RevSymCCId():
    """Connected Component Identifiers Container."""

    def __init__(self, _nb_distinct: int,
                 _cc_couples: list[tuple[IndexT, IndexT]],
                 _f_vertices_cc: list[Optional[tuple[IndexT, OrT]]],
                 ):
        """The Initializer."""
        # Number of disctint connected components
        self._nb_distinct: int = _nb_distinct
        # List of couples of connected component identifiers
        self._cc_couples: list[tuple[IndexT, IndexT]] = _cc_couples
        # List of forward vertices connected component identifier
        self._f_vertices_cc: list[Optional[tuple[IndexT, OrT]]] = (
            _f_vertices_cc
        )

    def card_cc(self) -> int:
        """Return the number of distinct connected components.

        Returns
        -------
        int
            Number of distinct connected components.
        """
        return self._nb_distinct

    def merged_orientations(self, vertex_index: IndexT) -> bool:
        """Return True if reversed is in the same connected component.

        Parameters
        ----------
        vertex_index : IndOrT
            Vertex index

        Returns
        -------
        bool
            Return True if the two orientations of a vertex
            are in the same connected component

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        NoConnectedComponentId
            If vertex is not associated with any connected component
        """
        try:
            cc_indor = self._f_vertices_cc[vertex_index]
        except IndexError as index_err:
            raise NoVertexIndex(vertex_index) from index_err
        if cc_indor is None:
            raise NoConnectedComponentId((vertex_index, FORWARD_INT))
        return (
            self._cc_couples[cc_indor[IND]][FORWARD_INT]
            == self._cc_couples[cc_indor[IND]][REVERSE_INT]
        )

    def reverse_cc(self, vertex: IndOrT) -> Optional[IndexT]:
        """Return the cc number of the `vertex` reverse.

        Parameters
        ----------
        vertex : IndOrT
            Oriented vertex

        Returns
        -------
        IndexT or None
            The connected component number (if exists, else None)

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            cc_indor = self._f_vertices_cc[vertex[IND]]
        except IndexError as index_err:
            raise NoVertexIndex(vertex[IND]) from index_err
        if cc_indor is not None:
            return self._cc_couples[cc_indor[IND]][
                FWDOR_REVOR[ORIENT_REV[vertex[OR]]][cc_indor[OR]]
            ]
        return None

    def __getitem__(self, vertex: IndOrT) -> Optional[IndexT]:
        """Return the cc number of oriented vertex.

        Parameters
        ----------
        vertex : IndOrT
            oriented vertex

        Returns
        -------
        IndexT or None
            Connected component identifier if exist or None

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            cc_indor = self._f_vertices_cc[vertex[IND]]
        except IndexError as index_err:
            raise NoVertexIndex(vertex[IND]) from index_err
        if cc_indor is not None:
            return self._cc_couples[cc_indor[IND]][
                FWDOR_REVOR[vertex[OR]][cc_indor[OR]]
            ]
        return None

    def __iter__(self) -> Iterator[
        tuple[
            IndOrT, Optional[IndexT],
            IndOrT, Optional[IndexT],
        ],
    ]:
        """Iter on both forward reverse vertices and their cc identifier.

        Yields
        ------
        IndOrT, int or None, IndorT, int or None
            Forward and reverse vertices
            and their connected component identifier
        """
        for v_ind, cc_indor in enumerate(self._f_vertices_cc):
            if cc_indor is None:
                v_cc = None
                v_rev_cc = None
            else:
                v_cc = self._cc_couples[cc_indor[IND]][cc_indor[OR]]
                v_rev_cc = self._cc_couples[cc_indor[IND]][
                    ORIENT_REV[cc_indor[OR]]
                ]
            yield (
                (v_ind, FORWARD_INT), v_cc,
                (v_ind, REVERSE_INT), v_rev_cc,
            )
