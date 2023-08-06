# -*- coding=utf-8 -*-

"""Global overlaps graph class file."""

from __future__ import annotations

from typing import Any, Optional

from revsymg.exceptions import NoGraphAttribute
from revsymg.graphs._adjancy_table import _AdjsT, _build_rev_sym_adj_table
from revsymg.graphs.revsym_edges import Edges
from revsymg.graphs.revsym_vertices import Vertices


# from revsymg.graphs.view.sub_edges import SubEdges
# from revsymg.graphs.view.sub_graph import SubRevSymGraph
# from revsymg.graphs.view.sub_vertices import SubVertices


# ============================================================================ #
#                                OVERLAPS GRAPH                                #
# ============================================================================ #
class RevSymGraph():
    """Reverse symmetric graph class.

    This graph is considering each orientation for all vertices and for
    all edges.
    It can contain several weakly connected components, which can contain
    only one strand or both merged.
    """

    _attributes: dict[str, Any]

    def __init__(self, attrs: Optional[dict[str, Any]] = None):
        """Initializer."""
        # Adjancies table ---
        adjs: _AdjsT = _build_rev_sym_adj_table()
        # Vertices container ---
        self._vertices: Vertices = Vertices(adjs)
        # Edges container ---
        self._edges: Edges = Edges(adjs)
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

    def is_attr(self, attrname: str) -> bool:
        """Return True if there is an attribute called attrname.

        Parameters
        ----------
        attrname : str
            Attribute's name answered

        Returns
        -------
        bool
            If there is an attribute called attrname
        """
        return attrname in self._attributes

    # -*- Subgraph methods -*-

    # def subgraph_from_vertices(self,
    #                         vertices: Iterable[IndOrT]) -> SubRevSymGraph:
    #     """Return a sub overlaps graph from vertices.

    #     Parameters
    #     ----------
    #     vertices : iterable of IndOrT
    #         An iterable of vertices

    #     Returns
    #     -------
    #     SubRevSymGraph
    #         The overlaps graph masked by vertices
    #     """
    #     sub_vertices = SubVertices(self._vertices)
    #     # REFACTOR: sub-edges should not have (sub-)vertices in parameter
    #     sub_edges = SubEdges(self._vertices, self._edges)
    #     for v in vertices:
    #         sub_vertices.add_to_mask(v)
    #     for v in sub_vertices:
    #         for w, e_ind in self._edges.succs(v):
    #             if w in sub_vertices:
    #                 sub_edges.add_to_mask(((v, w), e_ind))
    #     # REFACTOR: sub-vertex should get (sub-)vertex attributes, same for edges
    #     return SubRevSymGraph(
    #         sub_vertices, sub_edges,
    #         self._vertices._attributes, self._edges._attributes,
    #         self._attributes,
    #     )

    # def subgraph_from_edges(self,
    #                         edges: Iterable[EIndOrIndT]) -> SubRevSymGraph:
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
    #     sub_vertices = SubVertices(self._vertices)
    #     sub_edges = SubEdges(self._vertices, self._edges)
    #     for edge in edges:
    #         sub_vertices.add_to_mask(edge[EVERTICES][0])
    #         sub_vertices.add_to_mask(edge[EVERTICES][1])
    #         sub_edges.add_to_mask(edge)
    #     return SubRevSymGraph(
    #         sub_vertices, sub_edges,
    #         self._vertices._attributes, self._edges._attributes, self._attributes,
    #     )

    # -*- Getter -*-

    def vertices(self) -> Vertices:
        """Return the vertices container.

        Returns
        -------
        Vertices
            Vertices container
        """
        return self._vertices

    def edges(self) -> Edges:
        """Return the edge container.

        Returns
        -------
        Edges
            Edges container
        """
        return self._edges
