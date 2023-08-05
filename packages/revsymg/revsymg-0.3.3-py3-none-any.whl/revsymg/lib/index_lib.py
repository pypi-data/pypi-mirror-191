# -*- coding=utf-8 -*-

"""Types, constants and functions for indices module."""

from __future__ import annotations

from typing import Literal


# DOC: add custom type in docstring of constant or types
# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
# REFACTOR: separate & rename files to be more precise
#   - Base
#   - Reads
#   - Overlaps

# ---------------------------------------------------------------------------- #
#                                     Base                                     #
# ---------------------------------------------------------------------------- #
IndexT = int
"""Indices type."""

OrT = Literal[0, 1]
"""Orientations type.

Binary value
"""

# ---------------------------------------------------------------------------- #
#                                   Oriented                                   #
# ---------------------------------------------------------------------------- #
IndOrT = tuple[IndexT, OrT]
"""Vertices type.

type: :class:`tuple` (:data:`IndexT`, :data:`OrT`)
"""

EIndOrT = tuple[IndOrT, IndOrT]
"""Edges type with no edge index.

type: :class:`tuple` (:data:`IndOrT`, :data:`IndOrT`)
"""

EIndOrIndT = tuple[IndOrT, IndOrT, IndexT]
"""Edges with edge index type.

type: :class:`tuple` (:data:`IndOrT`, :data:`IndOrT`, :data:`IndexT`)
"""

IndOrIndT = tuple[IndOrT, IndexT]
"""Adjacent vertex with edge index type.

type: :class:`tuple` (:data:`IndOrT`, :data:`IndexT`)
"""

# ---------------------------------------------------------------------------- #
#                                 Non-oriented                                 #
# ---------------------------------------------------------------------------- #
EIndT = tuple[IndexT, IndexT]
"""Edges of indices type.

type: :class:`tuple` (:data:`IndexT`, :data:`IndexT`)
"""

EIndIndT = tuple[IndexT, IndexT, IndexT]
"""Edges of indices with edge index type.

type: :class:`tuple` (:data:`IndexT`, :data:`IndexT`, :data:`IndexT`)
"""

IndIndT = tuple[IndexT, IndexT]
"""Adjacent index vertex with edge index type.

type: :class:`tuple` (:data:`IndexT`, :data:`IndexT`)
"""

# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                             Fragment Orientations                            #
# ---------------------------------------------------------------------------- #
FORWARD_INT: OrT = 0
"""Forward orientation value.

type: :data:`OrT`
"""

REVERSE_INT: OrT = 1
"""Reverse orientation value.

type: :data:`OrT`
"""
#
# The list that gives the reverse value of a given orientation.
#
ORIENT_REV: tuple[OrT, OrT] = (REVERSE_INT, FORWARD_INT)
""":data:`OrT` reverse list.

type: :class:`tuple` (:data:`OrT`, :data:`OrT`)
"""
#
# For graph when ask oriented edges
#
FWDOR_REVOR: tuple[tuple[OrT, OrT], tuple[OrT, OrT]] = (
    (FORWARD_INT, REVERSE_INT),
    ORIENT_REV,
)
""":data:`OrT` relative orientation.

type: :class:`tuple` ((:data:`OrT`, :data:`OrT`), (:data:`OrT`, :data:`OrT`))
"""

# ---------------------------------------------------------------------------- #
#                                Oriented Vertex                               #
# ---------------------------------------------------------------------------- #
IND: Literal[0] = 0
"""The index for :data:`IndOrT`'s index value."""
OR: Literal[1] = 1
"""The index for :data:`IndOrT`'s orientation value."""

# ---------------------------------------------------------------------------- #
#                               Adjacencies Table                              #
# ---------------------------------------------------------------------------- #
PRED_IND: Literal[0] = 0
"""The index for predecessors of forwards in adjancies table"""
SUCC_IND: Literal[1] = 1
"""The index for successors of forwards in adjancies table"""

# ---------------------------------------------------------------------------- #
#                                Adjacency Type                                #
# ---------------------------------------------------------------------------- #
ADJ_INDOR: Literal[0] = 0
"""The index for :data:`IndOrT` value in :data:`IndOrIndT`."""
ADJ_IND: Literal[1] = 1
"""The index for :data:`IndexT` value in :data:`IndOrIndT`."""

# ---------------------------------------------------------------------------- #
#                             Edges And Edge Index                             #
# ---------------------------------------------------------------------------- #
U_INDOR: Literal[0] = 0
"""The index of first vertex in the edge."""

V_INDOR: Literal[1] = 1
"""The index of second vertex in the edge."""

E_IND: Literal[2] = 2
"""The index of edge's index in the edge.

For both :data:`EIndOrIndT` and :data:`EIndIndT` it corresponds to
:data:`IndexT` value.
"""

# ---------------------------------------------------------------------------- #
#                                 Miscellaneous                                #
# ---------------------------------------------------------------------------- #
MULT_IID: Literal[2] = 2
"""Index multiplier."""
# XXX: necessary?


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                    IndOrT                                    #
# ---------------------------------------------------------------------------- #
def is_forward(vertex: IndOrT) -> bool:
    """Return True if the `vertex` is considered as forward.

    Parameters
    ----------
    vertex : IndOrT
        A vertex

    Returns
    -------
    bool
        True if vertex's orientation is forward
    """
    return vertex[OR] == FORWARD_INT


def is_reverse(vertex: IndOrT) -> bool:
    """Return True if the `vertex` is considered as reverse.

    Parameters
    ----------
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    bool
        True is vertex is in reverse orientation
    """
    return vertex[OR] == REVERSE_INT


def rev_vertex(vertex: IndOrT) -> IndOrT:
    """Return the reverse vertex.

    Parameters
    ----------
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    IndOrT
        The reversed of vertex
    """
    return vertex[IND], ORIENT_REV[vertex[OR]]


# ---------------------------------------------------------------------------- #
#                                    EIndOrT                                   #
# ---------------------------------------------------------------------------- #
def rev_edge(first_vertex: IndOrT, second_vertex: IndOrT) -> EIndOrT:
    """Return the reverse edge.

    Parameters
    ----------
    first_vertex : IndOrT
        First oriented vertex in the edge
    second_vertex : IndOrT
        Second oriented vertex in the edge

    Returns
    -------
    EIndOrT
        The reversed of edge
    """
    return (
        (second_vertex[IND], ORIENT_REV[second_vertex[OR]]),
        (first_vertex[IND], ORIENT_REV[first_vertex[OR]]),
    )


def is_canonical(first_vertex: IndOrT, second_vertex: IndOrT) -> bool:
    r"""Xor boolean function between edge and its reverse.

    Parameters
    ----------
    first_vertex : IndOrT
        First oriented vertex in the edge
    second_vertex : IndOrT
        Second oriented vertex in the edge

    Returns
    -------
    bool
        True if :math:`\texttt{is_canonical}(\overline{edge})` is False,
        else False

    Notes
    -----
    :math:`\texttt{is_canonical}` is defined such as
    :math:`\texttt{is_canonical}(edge)
    \veebar \texttt{is_canonical}(\overline{edge})`
    """
    return (
        first_vertex[OR] == FORWARD_INT
        and (
            second_vertex[OR] == FORWARD_INT
            or first_vertex[IND] < second_vertex[IND]
        )
        or (
            second_vertex[OR] == FORWARD_INT
            and first_vertex[IND] < second_vertex[IND]
        )
    )


def eindor_orientation(first_vertex: IndOrT, second_vertex: IndOrT) -> OrT:
    """Return the edge orientation.

    Parameters
    ----------
    first_vertex : IndOrT
        First oriented vertex in the edge
    second_vertex : IndOrT
        Second oriented vertex in the edge

    Returns
    -------
    OrT
        Edge orientation

    Notes
    -----
    This is pure definition.
    Note that in case of self loop, return value is
    :const:`~revsymg.lib.index_lib.FORWARD_INT`
    """
    if first_vertex[IND] < second_vertex[IND]:
        return FORWARD_INT
    if first_vertex[IND] > second_vertex[IND]:
        return REVERSE_INT
    if first_vertex[OR] < second_vertex[OR]:
        return FORWARD_INT
    if first_vertex[OR] > second_vertex[OR]:
        return REVERSE_INT
    return first_vertex[OR]
