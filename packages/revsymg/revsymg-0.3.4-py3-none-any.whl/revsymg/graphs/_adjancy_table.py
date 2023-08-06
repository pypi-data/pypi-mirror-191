# -*- coding=utf-8 -*-

"""Protected adjancy symmetric reverse table module."""


from typing import Iterable

from revsymg.lib.index_lib import IND, OR, IndexT, IndIndT, IndOrIndT


# ============================================================================ #
#                                     TYPE                                     #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                            Reverse Symmetric Table                           #
# ---------------------------------------------------------------------------- #
_SubAdjT = list[IndOrIndT]

#   [PREDS_IND]: Predecessors lists
#       [v_index]: [(u_indor, e_ind) | (u_indor, v_indF) in E]
#   [SUCCS_IND]: Succesors lists
#       [u_index]: [(v_indor, e_ind) | (u_indF, v_indor) in E]
_AdjsT = tuple[
    list[_SubAdjT],
    list[_SubAdjT],
]


# ---------------------------------------------------------------------------- #
#                                 Indices Table                                #
# ---------------------------------------------------------------------------- #
_SubAdjIndT = list[IndIndT]

# [PREDS_IND]: Predecessors lists
#   [v_index]: [(u_ind, e_ind) | (u_ind, v_ind) in E]
# [SUCCS_IND]: Succesors lists
#   [u_index]: [(v_ind, e_ind) | (u_ind, v_ind) in E]
_AdjsIndT = tuple[
    list[_SubAdjIndT],
    list[_SubAdjIndT],
]


# ============================================================================ #
#                                   FUNCTION                                   #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                            Reverse Symmetric Table                           #
# ---------------------------------------------------------------------------- #
def _build_rev_sym_adj_table() -> _AdjsT:
    """Build empty symmetry reverse table for vertices/edges containers.

    Returns
    -------
    _AdjsT
        Symmetry reverse table
    """
    return ([], [])


def _shift_rev_sym_adj_table(sub_adj_tab: _SubAdjT,
                             pivot: IndexT) -> Iterable[IndOrIndT]:
    """Shift the sub adjancies table according pivot.

    Parameters
    ----------
    sub_adj_tab : _SubAdjT
        Sub-adjancies table
    pivot : IndexT
        Pivot index

    Yields
    ------
    IndOrIndT
        Shifted vertices indices
    """
    for indor, e_ind in sub_adj_tab:
        if indor[IND] != pivot:
            if indor[IND] > pivot:
                indor = (indor[IND] - 1, indor[OR])
            yield indor, e_ind


# ---------------------------------------------------------------------------- #
#                                 Indices Table                                #
# ---------------------------------------------------------------------------- #
def _build_indices_adj_table() -> _AdjsIndT:
    """Build empty indices table for vertices/edges containers.

    Returns
    -------
    _AdjsIndT
        Indices table
    """
    return ([], [])


def _shift_indices_adj_table(sub_adj_tab: _SubAdjIndT,
                             pivot: IndexT) -> Iterable[IndIndT]:
    """Shift the sub adjancies table according pivot.

    Parameters
    ----------
    sub_adj_tab : _SubAdjIndT
        Sub-adjancies table
    pivot : IndexT
        Pivot index

    Yields
    ------
    IndIndT
        Shifted vertices indices
    """
    for ind, e_ind in sub_adj_tab:
        if ind != pivot:
            if ind > pivot:
                ind = ind - 1
            yield ind, e_ind
