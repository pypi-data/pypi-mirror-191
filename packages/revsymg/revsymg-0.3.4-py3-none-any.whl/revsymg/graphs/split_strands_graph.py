# -*- coding=utf-8 -*-

"""Split strands overlaps graph class module."""

from __future__ import annotations

from typing import Any, Iterable, Optional

from bitarray import bitarray

from revsymg.exceptions import NoGraphAttribute
from revsymg.graphs._adjancy_table import _AdjsIndT, _build_indices_adj_table
from revsymg.graphs.split_strands_edges import SplitStrandsEdges
from revsymg.graphs.split_strands_vertices import SplitStrandsVertices
# from revsymg.graphs.view.sub_graph import SubRevSymGraph
from revsymg.lib.index_lib import EIndIndT, IndexT


# DOC: do doc for SplitStrandsGraph
# ============================================================================ #
#                       REVERSE SYMMETRIC OVERLAPS GRAPH                       #
# ============================================================================ #
class SplitStrandsGraph():
    r"""Graph containing only one DNA strand.

    For this graph :math:`G = (V, E)` we have:

    * :math:`\forall v \in V, \bar{v} \notin V`
    * :math:`\forall e \in E, \bar{e} \notin E`
    """

    def __init__(self, attrs: Optional[dict[str, Any]] = None):
        """Initializer."""
        # Adjancies table ---
        adjs: _AdjsIndT = _build_indices_adj_table()
        # Describe which orientation is in the arbitrary choosen connected comp.
        # - [v_ind]: FORWARD_INT | REVERSE_INT
        _cc: bitarray = bitarray()
        # Vertices container ---
        self._vertices: SplitStrandsVertices = SplitStrandsVertices(adjs, _cc)
        # Edges container ---
        self._edges: SplitStrandsEdges = SplitStrandsEdges(adjs, _cc)
        # Attributes container ---
        self._attributes: dict[str, Any] = attrs if attrs is not None else {}

    # -*- Graph methods -*-

    def attr(self, attrname: str) -> Any:
        """Return the value associated to attribute `attrname`.

        Parameters
        ----------
        attrname : str
            Attribute's name

        Returns
        -------
        Any
            Attribute value corresponding to the attribute name

        Raises
        ------
        NoGraphAttribute
            When there is no attribute key
        """
        try:
            return self._attributes[attrname]
        except KeyError as exc:
            raise NoGraphAttribute(attrname) from exc

    def attrs(self) -> dict[str, Any]:
        """Return the dictionnary of all attributes.

        Returns
        -------
        dict
            Dictionnary of attribute name as key and their value
        """
        return self._attributes

    def set_attr(self, attrname: str, attrvalue: Any):
        """Change the value of the attributes else create them.

        Parameters
        ----------
        attrname : str
            Attribute's name
        attrvalue : Any
            Attribute's value
        """
        self._attributes[attrname] = attrvalue

    # -*- Subgraph methods -*-

    # def subgraph_from_vertices(self, vertices: Iterable[IndexT]) -> SubRevSymGraph:
    #     """Return a sub overlaps graph from vertices.

    #     Parameters
    #     ----------
    #     vertices : iterable of IndexT
    #         An iterable of vertices

    #     Returns
    #     -------
    #     SubRevSymGraph
    #         The overlaps graph masked by vertices
    #     """
    #     raise NotImplementedError

    # def subgraph_from_edges(self,
    #                         edges: Iterable[EIndIndT]) -> SubRevSymGraph:
    #     """Return a sub overlaps graph from edges.

    #     Parameters
    #     ----------
    #     edges : iterable of EIndOrIndT
    #         An iterable of edges

    #     Returns
    #     -------
    #     SubRevSymGraph
    #         The overlaps graph masked by edges
    #     """
    #     raise NotImplementedError

    # -*- Getter -*-

    def vertices(self) -> SplitStrandsVertices:
        """Return the vertices container.

        Returns
        -------
        SplitStrandsVertices
            Vertices container
        """
        return self._vertices

    def edges(self) -> SplitStrandsEdges:
        """Return the edge container.

        Returns
        -------
        SplitStrandsEdges
            Edges container
        """
        return self._edges
