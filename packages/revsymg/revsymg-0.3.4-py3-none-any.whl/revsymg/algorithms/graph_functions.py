# -*- coding=utf-8 -*-

"""Algorithms for Symmetric Overlaps Graph."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from networkx import DiGraph as nx_DiGraph
from networkx import write_graphml as nx_write_graphml

from revsymg.exceptions import NoVertexIndex
from revsymg.graphs.merged_strands_graph import MergedStrandsRevSymGraph
from revsymg.graphs.revsym_graph import RevSymGraph
from revsymg.lib.index_lib import IND, OR, IndOrT
from revsymg.lib.str_lib import STRAND_STR


# ============================================================================ #
#                                    DEGREE                                    #
# ============================================================================ #
def in_degree(graph: Union[RevSymGraph, MergedStrandsRevSymGraph],
              vertex: IndOrT) -> int:
    """Return the in-degree of `vertex`.

    Parameters
    ----------
    graph : RevSymGraph or MergedStrandsRevSymGraph
        Reverse symmetric graph
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    int
        In-degree

    Raises
    ------
    NoVertexIndex
        If vertex does not exist in graph
    """
    try:
        return sum(1 for _ in graph.edges().preds(vertex))
    except NoVertexIndex as no_vertex_index:
        raise no_vertex_index


def out_degree(graph: Union[RevSymGraph, MergedStrandsRevSymGraph],
               vertex: IndOrT) -> int:
    """Return the out-degree of `vertex`.

    Parameters
    ----------
    graph : RevSymGraph or MergedStrandsRevSymGraph
        Reverse symmetric graph
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    int
        Out-degree

    Raises
    ------
    NoVertexIndex
        If vertex does not exist in graph
    """
    try:
        return sum(1 for _ in graph.edges().succs(vertex))
    except NoVertexIndex as no_vertex_index:
        raise no_vertex_index


def degree(graph: Union[RevSymGraph, MergedStrandsRevSymGraph],
           vertex: IndOrT) -> int:
    """Return the degree of `vertex`.

    Parameters
    ----------
    graph : RevSymGraph or MergedStrandsRevSymGraph
        Reverse symmetric graph
    vertex : IndOrT
        Oriented vertex

    Returns
    -------
    int
        Degree

    Raises
    ------
    NoVertexIndex
        If vertex does not exist in graph
    """
    try:
        return in_degree(graph, vertex) + out_degree(graph, vertex)
    except NoVertexIndex as no_vertex_index:
        raise no_vertex_index


# ============================================================================ #
#                           INPUTS-OUTPUTS FUNCTIONS                           #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                               Outputs Function                               #
# ---------------------------------------------------------------------------- #
def revsymg_to_graphml(graph: RevSymGraph, path: Path):
    """Save the graph as graphml format.

    Parameters
    ----------
    graph : RevSymGraph
        Reverse symmetric graph to output in graphml file format
    path : Path
        Output graphml path
    """
    vertices = graph.vertices()
    edges = graph.edges()
    di_graph = nx_DiGraph()
    for vertex in vertices:
        vertex_id = f'{vertex[IND]}{STRAND_STR[vertex[OR]]}'
        attrs = dict(vertices.attrs(vertex[IND]))
        di_graph.add_node(
            vertex_id, **attrs,
        )
    for u, v, e_ind in edges:
        u_id = f'{u[IND]}{STRAND_STR[u[OR]]}'
        v_id = f'{v[IND]}{STRAND_STR[v[OR]]}'
        attrs = dict(edges.attrs(e_ind))
        di_graph.add_edge(
            u_id, v_id, **attrs,
        )
    # Write graphml
    nx_write_graphml(di_graph, path)
