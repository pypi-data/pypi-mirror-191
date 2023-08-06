# -*- coding=utf-8 -*-

"""The connected component algorithms module."""

from __future__ import annotations

from queue import Queue
from typing import Optional, Union

from revsymg.algorithms.connected_components.cnnted_comp_id import (
    RevSymCCId,
    _RevSymCCIdFactory,
)
from revsymg.exceptions import NotNoneCCompId
from revsymg.graphs.merged_strands_graph import MergedStrandsRevSymGraph
from revsymg.graphs.revsym_graph import RevSymGraph
from revsymg.graphs.split_strands_graph import SplitStrandsGraph
from revsymg.graphs.split_strands_vertices import SplitStrandsVertices
# from revsymg.graphs.view.sub_graph import SubRevSymGraph
from revsymg.lib.index_lib import IND, OR, IndOrT


# ============================================================================ #
#                                     TYPES                                    #
# ============================================================================ #
GraphsT = Union[
    RevSymGraph,
    # SubRevSymGraph,
    MergedStrandsRevSymGraph,
    SplitStrandsGraph,
]
GraphsCnntedCompT = Union[
    SplitStrandsGraph,
    MergedStrandsRevSymGraph,
]


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                        Redundant Connected Components                        #
# ---------------------------------------------------------------------------- #
def connected_components(graph: RevSymGraph) -> RevSymCCId:
    """Return the cc of each vertex.

    Parameters
    ----------
    graph : RevSymGraph
        The reverse symmetric graph

    Returns
    -------
    RevSymCCId
        A connected component identifiers container
    """
    ccompcont = _RevSymCCIdFactory(graph.vertices().card_index())
    for u in graph.vertices():
        if ccompcont[u] is None:  # Not explored nor its reverse yet
            ccompcont.new_cc_couple()
            __explore_weak(graph, u, ccompcont)

    return ccompcont.to_readonly_view()


def __explore_weak(graph: RevSymGraph, u: IndOrT,
                   ccompcont: _RevSymCCIdFactory):
    """Explore the `cc`-th connected component from `u`."""
    edges = graph.edges()
    lifo: Queue = Queue()
    lifo.put(u)
    ccompcont.set_cc_id(u)
    while not lifo.empty():
        u = lifo.get()
        for v, _ in edges.neighbours(u):
            #
            # Not explored nor its reverse yet
            #
            if ccompcont[v] is None:
                ccompcont.set_cc_id(v)
                lifo.put(v)
            #
            # Reverse of an already explored: two strands are confused in cc
            #
            elif not ccompcont.continuity(v):
                ccompcont.merge_cc()


# ---------------------------------------------------------------------------- #
#                      Non-redundant Connected Components                      #
# ---------------------------------------------------------------------------- #
# def nonredundant_connected_components(
#         ccompcont: RevSymCCId) -> CnntedComplistT:
#     r"""Return the connected components without redundance.

#     Requires that :math:`\forall v \in V, cc(v) \neq None`

#     - Use only one oriented
#       :class:`~revsymg.algorithms.connected_components.cnnted_comp_cls.SplitStrandsCnntedComp`
#       between two existing *i.e.* if :math:`cc(v) != cc(v')` then only keep
#       one connected component (because the other can be found from the other)

#     - Use :class:`~revsymg.algorithms.connected_components.cnnted_comp_cls.MergedStrandsCnntedComp`
#       in which it is known that :math:`v` and :math:`v'` are in the same
#       connected component

#     Parameters
#     ----------
#     ccompcont : RevSymCCId
#         The connected component identifier container

#     Returns
#     -------
#     list of SplitStrandsCnntedComp or MergedStrandsCnntedComp
#         List of simple or double connected component

#     Raises
#     ------
#     NotNoneCCompId
#         If :math:`\exists v \in V \mid cc(v) = None`
#     """  # noqa: E501 (too long line)
#     #
#     # Initialisation
#     #
#     n_redundant_cc = ccompcont.card_cc()
#     cc_to_keep: list[Optional[bool]] = [None for _ in range(n_redundant_cc)]
#     n_new_cc = 0  # [num_cc original] = new num_cc
#     #
#     # l_cc_trans[cc_ind]:
#     #   = None if cc_ind not yet discovered
#     #   = new_cc_ind >= 0 if already cc_ind already discovered
#     #   = -1 if cc_ind is not kept
#     l_cc_trans: list[Optional[int]] = [None for _ in range(n_redundant_cc)]
#     l_ccs: CnntedComplistT = []  # connected comp. kept
#     #
#     # Loop on vertices and their cc id
#     #
#     for v, v_cc, v_rev, v_rev_cc in ccompcont:
#         #
#         # cc ids must be not None
#         #
#         if v_cc is None or v_rev_cc is None:
#             raise NotNoneCCompId(v, v_cc, v_rev, v_rev_cc)
#         #
#         # Undiscovered cc
#         #
#         if cc_to_keep[v_cc] is None:
#             cc_to_keep[v_cc] = True
#             l_cc_trans[v_cc] = n_new_cc
#             #
#             # Simple cc
#             #
#             if v_rev_cc != v_cc:
#                 l_ccs.append(SplitStrandsCnntedComp(n_new_cc, v))
#                 cc_to_keep[v_rev_cc] = False
#             #
#             # Double cc
#             #
#             else:
#                 l_ccs.append(MergedStrandsCnntedComp(n_new_cc, v))
#             n_new_cc += 1
#         #
#         # Already discovered cc
#         #
#         else:
#             if cc_to_keep[v_cc]:
#                 new_num_cc: int = l_cc_trans[v_cc]  # type: ignore
#                 l_ccs[new_num_cc].add(v)
#             elif cc_to_keep[v_rev_cc]:
#                 # This is elif because we don't want to add twice v in double cc
#                 #   but add v in the kept complementary simple cc
#                 new_num_cc: int = l_cc_trans[v_rev_cc]  # type: ignore
#                 l_ccs[new_num_cc].add(v_rev)
#     return l_ccs


# def connected_comp_to_graphs(graph: RevSymGraph,
#                              ccompcont: RevSymCCId,
#                              ) -> list[GraphsCnntedCompT]:
#     r"""Returns one graph for each connected component.

#     Requires that :math:`\forall v \in V, cc(v) \neq None`

#     Parameters
#     ----------
#     graph : RevSymGraph
#         Reverse symmetric graph
#     ccompcont : RevSymCCId
#         Connected component identifiers container

#     Returns
#     -------
#     list of SplitStrandsGraph or MergedStrandsRevSymGraph
#         One graph for each (symmetric or merged) connected component

#     Raises
#     ------
#     NotNoneCCompId
#         If :math:`\exists v \in V \mid cc(v) = None`
#     """
#     # TODO: indices of vertices will change (and those of edges too)
#     #   Find a way to associate old and new indices
#     #
#     # Initialisation
#     #
#     n_redundant_cc = ccompcont.card_cc()
#     n_new_cc = 0  # [num_cc original] = new num_cc
#     #
#     # l_cc_trans[cc_ind]:
#     #   = None if cc_ind not yet discovered
#     #   = new_cc_ind >= 0 if already cc_ind already discovered
#     #   = -1 if cc_ind is not kept
#     l_cc_trans: list[Optional[int]] = [None for _ in range(n_redundant_cc)]
#     graph_ccs: list[GraphsCnntedCompT] = []
#     #
#     # Loop on vertices and their cc id
#     #
#     for v, v_cc, v_rev, v_rev_cc in ccompcont:
#         #
#         # cc ids must be not None
#         #
#         if v_cc is None or v_rev_cc is None:
#             raise NotNoneCCompId(v, v_cc, v_rev, v_rev_cc)
#         #
#         # Undiscovered cc
#         #
#         if l_cc_trans[v_cc] is None:
#             l_cc_trans[v_cc] = n_new_cc
#             graph_cc: GraphsCnntedCompT
#             #
#             # Symmetric cc
#             #
#             if v_rev_cc != v_cc:
#                 graph_cc = SplitStrandsGraph()
#                 l_cc_trans[v_rev_cc] = -1
#             #
#             # Merged cc
#             #
#             else:
#                 graph_cc = MergedStrandsRevSymGraph()
#             __add_adj_graph_cc(graph, graph_cc, v)
#             graph_ccs.append(graph_cc)
#             n_new_cc += 1
#         #
#         # Already discovered cc
#         #
#         elif l_cc_trans[v_cc] < 0:  # type: ignore
#             # Reverse sym cc with arbitrarly v_rev_cc kept
#             __add_adj_graph_cc(
#                 graph, graph_ccs[l_cc_trans[v_rev_cc]], v_rev,  # type: ignore
#             )

#         else:
#             #
#             # v_cc kept
#             #
#             __add_adj_graph_cc(
#                 graph, graph_ccs[l_cc_trans[v_cc]], v,  # type: ignore
#             )
#             #
#             # Must add edges for the reverse bc reverse merged
#             #
#             if v_cc == v_rev_cc:
#                 __add_adj_graph_cc(
#                     graph, graph_ccs[l_cc_trans[v_rev_cc]],  # type: ignore
#                     v_rev,
#                 )

#     return graph_ccs


# def __add_adj_graph_cc(graph: RevSymGraph, graph_cc: GraphsCnntedCompT,
#                        vertex: IndOrT):
#     """Add `v` adjencies edges to `graph_cc`.

#     Parameters
#     ----------
#     graph : RevSymGraph
#         Reverse symmetric graph
#     graph_cc : SplitStrandsOverlapsgraph or MergedStrandsRevSymGraph
#         Connected component graph
#     vertex : IndOrT
#         Oriented vertex
#     """
#     vertices = graph.vertices()
#     edges = graph.edges()
#     new_vertices = graph_cc.vertices()
#     new_edges = graph_cc.edges()
#     if isinstance(new_vertices, SplitStrandsVertices):
#         v_new_ind = new_vertices.add(vertex[OR])
#     else:
#         v_new_ind = new_vertices.add()
#     # XXX: be sure to add attr before!
#     for attrname, attrvalue in vertices.attrs(vertex[IND]):
#         new_vertices.set_attr(v_new_ind, attrname, attrvalue)
#     for w, e_ind in edges.succs(vertex):
#         w_new =
#         graph_cc.add_overlap(
#             (v_new, w_new), **edges.attrs(((v, w), e_ind)),
#         )
