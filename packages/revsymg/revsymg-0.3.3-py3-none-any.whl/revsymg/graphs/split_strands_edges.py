# -*- coding=utf-8 -*-

"""Split strands edges container class module."""

from __future__ import annotations

from typing import Any, Iterator

from bitarray import bitarray

from revsymg.exceptions import (
    NoEdgeIndex,
    NoEdgesAttribute,
    NoIndicesEdge,
    NoVertexIndex,
    WrongAttributeType,
    _NoAttribute,
    _NoKey,
)
from revsymg.graphs._adjancy_table import _AdjsIndT
from revsymg.graphs.attributes import AttributesContainer
from revsymg.lib.index_lib import (
    PRED_IND,
    SUCC_IND,
    EIndIndT,
    EIndT,
    IndexT,
    IndIndT,
)


# DOC: do doc for SplitStrandsEdges
# ============================================================================ #
#                         SPLIT STRANDS EDGES CONTAINER                        #
# ============================================================================ #
class SplitStrandsEdges():
    r"""Unique oriented edges container.

    This edges container is containing only one orientation for each of its
    edge *i.e.* :math:`\forall e \in E, \bar{e} \notin E`

    Warnings
    --------
    You must not instantiate a Edges object.
    Use it only for typing or get an already instanciated object.
    """

    def __init__(self, _adjs: _AdjsIndT, _cc: bitarray):
        """The Initializer."""
        # The number of current edges
        self._card_e: int = 0
        # The last edges integer identifier ---
        self._ind_e: IndexT = -1
        # Adjancies table ---------------------------------
        #
        # [PREDS_IND]: Predecessors lists
        #   [v_index]: [(u_ind, e_ind) | (u_ind, v_ind) in E]
        # [SUCCS_IND]: Succesors lists
        #   [u_index]: [(v_ind, e_ind) | (u_ind, v_ind) in E]
        #
        self._adjs: _AdjsIndT = _adjs
        # Describe the vertices' orientation
        #   [v_ind]: FORWARD_INT | REVERSE_INT
        self._cc: bitarray = _cc  # XXX: just for cheking exc but not necessary
        # Attributes for edges
        self._attributes: AttributesContainer = AttributesContainer()

    # -*- Attributes -*-

    def attr(self, edge_index: IndexT, attrname: str) -> Any:
        """Return the edge attribute `attrname`.

        Parameters
        ----------
        edge_index: IndexT
            Edge's index
        attrname: str
            Attribute name

        Returns
        -------
        Any
            Attribute value

        Raises
        ------
        NoEdgeIndex
            If edge does not exist
        NoEdgesAttribute
            If there is no attribute name like this for edges

        Note
        ----
        A removed edge still have a recorded attribute.
        """
        try:
            return self._attributes.get(edge_index, attrname)
        except _NoAttribute as exc:
            raise NoEdgesAttribute(attrname) from exc
        except _NoKey as exc:
            raise NoEdgeIndex(edge_index) from exc

    def attrs(self, edge_index: IndexT) -> Iterator[tuple[str, Any]]:
        """Iterate over all edge's attributes.

        Parameters
        ----------
        edge_index: IndexT
            Edge's index

        Yields
        ------
        str
            Attribute's name
        Any
            Attribute's value

        Raises
        ------
        NoEdgeIndex
            If there is no edge index

        Note
        ----
        A removed edge still have a recorded attribute.
        """
        try:
            yield from self._attributes.get_all(edge_index)
        except _NoKey as _no_key:
            raise NoEdgeIndex(edge_index) from _no_key

    def new_attr(self, attrname: str, default: Any):
        """Add an attribute entry.

        Parameters
        ----------
        attrname : str
            Attribute's name
        default : Any
            Default attribute value

        Note
        ----
        Before setting attribute to one edge, it is necessary to add
        an attribute entry using this method.
        """
        self._attributes.new_attr(attrname, default)

    def set_attr(self, edge_index: IndexT, attrname: str, attrvalue: Any):
        """Change the value of one attribute.

        Parameters
        ----------
        edge_index : IndexT
            Edge's index
        attrname : str
            Attribute's name
        attrvalue : Any
            Attribute's value

        Raises
        ------
        NoEdgesAttribute
            If there is no attribute nammed like this for edges
        WrongAttributeType
            Given value does not correspond to attribute's type
        NoEdgeIndex
            If there is no vertex index

        Note
        ----
        Be sure having added an attribute entry using the method
        :meth:`~revsymg.Vertices.new_attr`
        """
        try:
            self._attributes.set_attr(edge_index, attrname, attrvalue)
        except _NoAttribute as _no_attr:
            raise NoEdgesAttribute(attrname) from _no_attr
        except WrongAttributeType as wrong_attr_type:
            raise wrong_attr_type
        except _NoKey as _no_key:
            raise NoEdgeIndex(edge_index) from _no_key

    # -*- Getter -*-

    def eindor_to_eind(self, first_vertex: IndexT,
                       second_vertex: IndexT) -> Iterator[IndexT]:
        """Iterate over edge index from indices edge.

        Parameters
        ----------
        first_vertex : IndexT
            First vertex
        second_vertex : IndexT
            Second vertex

        Yields
        ------
        IndexT
            Edge index

        Raises
        ------
        NoVertexIndex
            One of the vertex in edge does not exist
        """
        #
        # Exceptions
        #
        if first_vertex >= len(self._cc):
            raise NoVertexIndex(first_vertex)
        if second_vertex >= len(self._cc):
            raise NoVertexIndex(second_vertex)
        #
        # Search
        #
        yield from (
            e_ind
            for succ, e_ind in self._adjs[SUCC_IND][first_vertex]
            if succ == second_vertex
        )

    # -*- Edges -*-

    def preds(self, vertex: IndexT) -> Iterator[IndIndT]:
        """Iterate over vertex's predecessors.

        Parameters
        ----------
        vertex: IndexT
            Vertex's index

        Yields
        ------
        IndIndT
            Predecessor vertex's index with edge index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            preds = self._adjs[PRED_IND][vertex]
        except IndexError as exc:
            raise NoVertexIndex(vertex) from exc
        yield from preds

    def succs(self, vertex: IndexT) -> Iterator[IndIndT]:
        """Iterate over vertex's successors.

        Parameters
        ----------
        vertex: IndexT
            Vertex's index

        Yields
        ------
        IndIndT
            Successors vertex's index with edge index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            succs = self._adjs[SUCC_IND][vertex]
        except IndexError as exc:
            raise NoVertexIndex(vertex) from exc
        yield from succs

    def neighbours(self, vertex: IndexT) -> Iterator[IndIndT]:
        """Iterate over `vertex`'s adjacencies vertices.

        Parameters
        ----------
        vertex: IndexT
            Vertex's index

        Yields
        ------
        IndIndT
            Adjacent vertices's index with edge index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        try:
            yield from self.preds(vertex)
            yield from self.succs(vertex)
        except NoVertexIndex as no_vertex_index:
            raise no_vertex_index

    # -*- Setter -*-

    def add(self, first_vertex: IndexT, second_vertex: IndexT) -> IndexT:
        """Add `edge` to edges.

        Parameters
        ----------
        first_vertex : IndexT
            First vertex
        second_vertex : IndexT
            Second vertex

        Returns
        -------
        IndexT
            Edge index

        Raises
        ------
        NoVertexIndex
            If one vertex does not exist
        """
        #
        # Exceptions
        #
        if len(self._adjs[PRED_IND]) <= first_vertex:
            raise NoVertexIndex(first_vertex)
        if len(self._adjs[PRED_IND]) <= second_vertex:
            raise NoVertexIndex(second_vertex)
        self._ind_e += 1
        #
        # Successor
        #
        self._adjs[SUCC_IND][first_vertex].append(
            (second_vertex, self._ind_e),
        )
        #
        # Predecessor
        #
        self._adjs[PRED_IND][second_vertex].append(
            (first_vertex, self._ind_e),
        )
        self._card_e += 1
        self._attributes.add_keys(1)
        return self._ind_e

    def delete(self, first_vertex: IndexT, second_vertex: IndexT,
               edge_index: IndexT):
        r"""Remove the edge.

        Parameters
        ----------
        first_vertex : IndexT
            First vertex
        second_vertex : IndexT
            Second vertex
        edge_index : IndexT
            Edge's index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        NoIndicesEdge
            If there is no recorded edge with these vertices and this index

        Note
        ----
        When deleting, the edge is replacing by the last one in adjancy list,
        and the last element of the adjancy list is removed.
        """
        #
        # Exceptions
        #
        if first_vertex >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(first_vertex)
        if second_vertex >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(second_vertex)
        #
        # Delete u from v's predecessors
        #
        u_adj: IndIndT = (first_vertex, edge_index)
        try:
            adj_ind = self._adjs[PRED_IND][second_vertex].index(u_adj)
            # by symmetry, other index method bellow will raises ValueError too
        except ValueError as value_error:
            raise NoIndicesEdge(
                first_vertex, second_vertex, edge_index,
            ) from value_error
        if adj_ind < len(self._adjs[PRED_IND][second_vertex]) - 1:
            self._adjs[PRED_IND][second_vertex][adj_ind] = (
                self._adjs[PRED_IND][second_vertex].pop()
            )
        else:
            self._adjs[PRED_IND][second_vertex].pop()
        #
        # Delete v from u's successors
        #
        v_adj: IndIndT = (second_vertex, edge_index)
        adj_ind = self._adjs[SUCC_IND][first_vertex].index(v_adj)
        if adj_ind < len(self._adjs[SUCC_IND][first_vertex]) - 1:
            self._adjs[SUCC_IND][first_vertex][adj_ind] = (
                self._adjs[SUCC_IND][first_vertex].pop()
            )
        else:
            self._adjs[SUCC_IND][first_vertex].pop()
        self._card_e -= 1

    # -*- Overloaded built-in -*-

    def __iter__(self) -> Iterator[EIndIndT]:
        """Iterate over indices edges with edge index.

        Yields
        ------
        EIndIndT
            Indices edges with their edge index
        """
        for v in range(len(self._cc)):
            for w, e_ind in self._adjs[SUCC_IND][v]:
                yield v, w, e_ind

    def __contains__(self, edge: EIndT) -> bool:
        """Return True if the indices edge is in edges container.

        Parameters
        ----------
        edge: EIndT
            Indices edge

        Returns
        -------
        bool
            Indices edge in edges container
        """
        u, v = edge
        #
        # No vertices
        #
        if len(self._cc) <= u:
            return False
        if len(self._cc) <= v:
            return False
        #
        # Search in forward's successors table
        #
        return any(v == succ for succ, _ in self._adjs[SUCC_IND][u])

    def __len__(self) -> int:
        r"""Return the number of edges.

        Returns
        -------
        int
            Number of edges

        Notes
        -----
        :math:`\forall e \in E, \bar{e} \notin E`
        """
        return self._card_e
