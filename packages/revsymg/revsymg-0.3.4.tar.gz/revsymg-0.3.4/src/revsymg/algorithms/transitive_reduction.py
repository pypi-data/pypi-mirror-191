# # -*- coding=utf-8 -*-

"""Transitive edges removal algo."""


from typing import Literal

from revsymg.graphs.revsym_graph import RevSymGraph
from revsymg.lib.index_lib import IND, IndOrT


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
# REFACTOR: move these constants?
FUZZ: Literal[10] = 10
"""Constant for upper-bound."""

READ_LEN_STR = 'read_length'
"""Vertex attribute name coresponding to read length."""

OV_LEN_STR = 'overlap_length'
"""Edge attribute name corresponding to overlap length."""

_VACANT = 0
_INPLAY = 1
_ELIMINATED = 2


# ============================================================================ #
#                                 MAIN FUNCTION                                #
# ============================================================================ #
def transitive_reduction(ovg: RevSymGraph, fuzz: int = FUZZ,
                         read_len_str: str = READ_LEN_STR,
                         ov_len_str: str = OV_LEN_STR):
    """Remove transitive edges.

    Parameters
    ----------
    ovg : RevSymGraph
        Overlaps graph
    fuzz : int, default FUZZ
        Constant for upper-bound
    read_len_str : str, default READ_LEN_STR
        Vertex attribute name coresponding to read length
    ov_len_str : str, default OV_LEN_STR
        Edge attribute name corresponding to overlap length

    Warning
    -------
    For each pair oriented vertices :math:`u` and :math:`v` there is
    **at most one** overlap.
    """
    # NOTE: do proof concerning non-colision in indices
    #   - especially concerning tandem and return of self
    l_mark = [_VACANT] * len(ovg.vertices())

    for v in ovg.vertices():

        lt_edges = __one_top_neighbors(ovg, v, read_len_str, ov_len_str)

        longest = lt_edges[-1][1] + fuzz if lt_edges else 0
        # -------------------------------------------------------------------- #
        # Detect transitive edges
        # -------------------------------------------------------------------- #
        for w, _ in lt_edges:
            l_mark[w[IND]] = _INPLAY

        for w, w_suffix in lt_edges:

            lt_2_edges = __two_top_neighbors(
                ovg, w, l_mark, read_len_str, ov_len_str,
            )

            for k, (x, x_suffix) in enumerate(lt_2_edges):

                if (l_mark[w[IND]] == _INPLAY
                        and w_suffix + x_suffix <= longest):
                    l_mark[x[IND]] = _ELIMINATED
                # pylint: disable=compare-to-zero
                if x_suffix < fuzz or k == 0:
                    l_mark[x[IND]] = _ELIMINATED
        # -------------------------------------------------------------------- #
        # Remove transitive edges
        # -------------------------------------------------------------------- #
        for w, e_ind in ovg.edges().succs(v):
            if l_mark[w[IND]] == _ELIMINATED:
                # XXX: proof rev delete
                ovg.edges().delete(v, w, e_ind)
            l_mark[w[IND]] = _VACANT


def __one_top_neighbors(ovg: RevSymGraph,
                        v: IndOrT, read_len_str: str,
                        ov_len_str: str) -> list[tuple[IndOrT, int]]:
    """Return the one-top neighbour of `v` sorted by suffix length.

    Parameters
    ----------
    ovg : RevSymGraph
        Overlaps graph
    v : IndOrT
        Oriented vertex
    read_len_str : str
        Attribute name for read's length
    ov_len_str : str
        Attribute name for overlap's length

    Returns
    -------
    list of IndOrT, int
        List of sorted successors and their suffix length
    """
    lt_edges: list[tuple[IndOrT, int]] = []

    for w, e_ind in ovg.edges().succs(v):

        w_suffix = max(
            0,
            ovg.vertices().attr(w[IND], read_len_str)
            - ovg.edges().attr(e_ind, ov_len_str),
        )
        lt_edges.append((w, w_suffix))

    return sorted(lt_edges, key=lambda t: t[1])


def __two_top_neighbors(ovg: RevSymGraph, w: IndOrT,
                        l_mark: list[int], read_len_str: str,
                        ov_len_str: str) -> list[tuple[IndOrT, int]]:
    """Return the one-top neighbors of `w` sorted by suffix length.

    Parameters
    ----------
    ovg : RevSymGraph
        Overlaps graph
    w : IndOrT
        Oriented vertex
    l_mark : list of int
        Vertices states
    read_len_str : str
        Attribute name for read's length
    ov_len_str : str
        Attribute name for overlap's length

    Returns
    -------
    list of IndOrT, int
        List of sorted successors and their suffix length
    """
    lt_edges: list[tuple[IndOrT, int]] = []

    for x, e_ind in ovg.edges().succs(w):
        if l_mark[x[IND]] == _INPLAY:
            x_suffix = max(
                0,
                ovg.vertices().attr(x[IND], read_len_str)
                - ovg.edges().attr(e_ind, ov_len_str),
            )
            lt_edges.append((x, x_suffix))

    return sorted(lt_edges, key=lambda t: t[1])
