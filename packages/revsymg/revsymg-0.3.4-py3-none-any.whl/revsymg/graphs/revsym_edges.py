# -*- coding=utf-8 -*-

"""Global edges container class module."""

from __future__ import annotations

from typing import Any, Iterator

from revsymg.exceptions import (
    NoEdge,
    NoEdgeIndex,
    NoEdgesAttribute,
    NoVertexIndex,
    WrongAttributeType,
    _NoAttribute,
    _NoKey,
)
from revsymg.graphs._adjancy_table import _AdjsT
from revsymg.graphs.attributes import AttributesContainer
from revsymg.lib.index_lib import (
    FORWARD_INT,
    FWDOR_REVOR,
    IND,
    OR,
    ORIENT_REV,
    PRED_IND,
    REVERSE_INT,
    SUCC_IND,
    EIndOrIndT,
    EIndOrT,
    IndexT,
    IndOrIndT,
    IndOrT,
)


# ============================================================================ #
#                                EDGES CONTAINER                               #
# ============================================================================ #
class Edges():
    r"""Edges container class for both edges' orientations.

    For each overlap :math:`o \in \mathcal{O}`, there are two edges
    :math:`e \in E` and :math:`\bar{e} \in E` *i.e.* one for both orientations.

    Warnings
    --------
    You must not call this class.
    Use it only for typing or get an already existing object.
    """

    def __init__(self, _adjs: _AdjsT):
        """The Initializer."""
        #
        # The number of current edges
        #
        self._card_e: int = 0
        #
        # The last edge integer identifier
        #
        self._ind_e: IndexT = -1  # FIXME: change to be always | 2 as described
        #
        # Adjancies table
        #
        # [PREDS_IND]: Predecessors lists
        #   [v_index]: [(u_indor, e_ind) | (u_indor, v_indF) in E]
        # [SUCCS_IND]: Succesors lists
        #   [u_index]: [(v_indor, e_ind) | (u_indF, v_indor) in E]
        #
        self._adjs: _AdjsT = _adjs
        #
        # Attributes container
        #
        self._attributes: AttributesContainer = (
            AttributesContainer()
        )

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

    def biggest_edge_index(self) -> int:
        """Return the biggest edge index.

        Returns
        -------
        int
            The biggest edge index

        Notes
        -----
        The number of distinct edges indices is equal to
        the biggest edge index plus one.
        """
        return self._ind_e

    def eindor_to_eind(self, first_vertex: IndOrT,
                       second_vertex: IndOrT) -> Iterator[IndexT]:
        """Iterate over edge indices from oriented edge.

        Parameters
        ----------
        first_vertex : IndOrT
            First oriented vertex
        second_vertex : IndOrT
            Second oriented vertex

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
        if first_vertex[IND] >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(first_vertex[IND])
        if second_vertex[IND] >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(second_vertex[IND])
        #
        # Search
        #
        if first_vertex[OR] == FORWARD_INT:
            yield from (
                e_ind
                for succ, e_ind in self._adjs[SUCC_IND][first_vertex[IND]]
                if succ == second_vertex
            )
        else:
            v_rev = second_vertex[IND], ORIENT_REV[second_vertex[OR]]
            yield from (
                e_ind
                for pre_rev, e_ind in self._adjs[PRED_IND][first_vertex[IND]]
                if pre_rev == v_rev
            )

    # -*- Iteration -*-

    def preds(self, vertex: IndOrT) -> Iterator[IndOrIndT]:
        """Iterate over vertex's predecessors.

        Parameters
        ----------
        vertex: IndOrT
            Oriented vertex

        Yields
        ------
        IndOrIndT
            Predecessor oriented vertex with edge index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        if vertex[OR] == FORWARD_INT:
            try:
                yield from self._adjs[PRED_IND][vertex[IND]]
            except IndexError as exc:
                raise NoVertexIndex(vertex[IND]) from exc
        else:
            try:
                for succ_rev, e_ind in self._adjs[SUCC_IND][vertex[IND]]:
                    yield (succ_rev[IND], ORIENT_REV[succ_rev[OR]]), e_ind
            except IndexError as exc:
                raise NoVertexIndex(vertex[IND]) from exc

    def succs(self, vertex: IndOrT) -> Iterator[IndOrIndT]:
        """Iterate over vertex's successors.

        Parameters
        ----------
        vertex: IndOrT
            Oriented vertex

        Yields
        ------
        IndOrIndT
            Successor oriented vertex with edge index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        """
        if vertex[OR] == FORWARD_INT:
            try:
                yield from self._adjs[SUCC_IND][vertex[IND]]
            except IndexError as exc:
                raise NoVertexIndex(vertex[IND]) from exc
        else:
            try:
                for pred_rev, e_ind in self._adjs[PRED_IND][vertex[IND]]:
                    yield (pred_rev[IND], ORIENT_REV[pred_rev[OR]]), e_ind
            except IndexError as exc:
                raise NoVertexIndex(vertex[IND]) from exc

    def neighbours(self, vertex: IndOrT) -> Iterator[IndOrIndT]:
        """Return the generator of `vertex`'s adjacencies vertices.

        Parameters
        ----------
        vertex: IndOrT
            Oriented vertex

        Yields
        ------
        IndOrIndT
            Oriented neighbouring vertices with edge index

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

    def add(self, first_vertex: IndOrT, second_vertex: IndOrT) -> IndexT:
        r"""Add an edge to edges container.

        Parameters
        ----------
        first_vertex : IndOrT
            First oriented vertex
        second_vertex : IndOrT
            Second oriented vertex

        Returns
        -------
        IndexT
            Edge index

        Raises
        ------
        NoVertexIndex
            If one vertex does not exist

        Notes
        -----
        Edges container contains the two orientations of each edge *i.e.*
        :math:`\forall e \in E, \bar{e} \in E`
        """
        #
        # Exceptions
        #
        if first_vertex[IND] >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(first_vertex[IND])
        if second_vertex[IND] >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(second_vertex[IND])
        self._ind_e += 1
        #
        # Successor
        #
        if first_vertex[OR] == FORWARD_INT:  # (u_f, v_f-r)
            self._adjs[SUCC_IND][first_vertex[IND]].append(
                (second_vertex, self._ind_e),
            )
        else:  # (u_r, v_f-r)
            v_r = second_vertex[IND], ORIENT_REV[second_vertex[OR]]
            self._adjs[PRED_IND][first_vertex[IND]].append(
                (v_r, self._ind_e),
            )
        #
        # Predecessor
        #
        if second_vertex[OR] == FORWARD_INT:  # (u_f-r, v_f)
            self._adjs[PRED_IND][second_vertex[IND]].append(
                (first_vertex, self._ind_e),
            )
        else:  # (u_f-r, v_r)
            u_r = first_vertex[IND], ORIENT_REV[first_vertex[OR]]
            self._adjs[SUCC_IND][second_vertex[IND]].append(
                (u_r, self._ind_e),
            )
        self._card_e += 1
        self._attributes.add_keys(1)
        return self._ind_e

    def delete(self, first_vertex: IndOrT, second_vertex: IndOrT,
               edge_index: IndexT):
        r"""Remove the edge.

        Parameters
        ----------
        first_vertex : IndOrT
            First oriented vertex
        second_vertex : IndOrT
            Second oriented vertex
        edge_index : IndexT
            Edge's index

        Raises
        ------
        NoVertexIndex
            If vertex does not exist
        NoEdge
            If there is no recorded edge with these vertices and this index

        Note
        ----
        When deleting, the edge is replacing by the last one in adjancy list,
        and the last element of the adjancy list is removed.

        Warning
        -------
        As :class::`revsymg.graphs.Edges` has the reverse symmetry property,
        removing one orientation of an edge has the consequence of removing the
        other orientation *i.e.*
        :math:`\forall e \in E, \bar{e} \notin E \setminus \{e\}`
        """
        # DOC: do a figure
        # XXX: change edge index? -> if so, do a figure
        #
        # Exceptions
        #
        if first_vertex[IND] >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(first_vertex[IND])
        if second_vertex[IND] >= len(self._adjs[PRED_IND]):
            raise NoVertexIndex(second_vertex[IND])
        #
        # Delete u from v's predecessors
        #
        u_adj: IndOrIndT = (
            (
                first_vertex[IND],
                FWDOR_REVOR[second_vertex[OR]][first_vertex[OR]],
            ),
            edge_index,
        )
        pred_ind = FWDOR_REVOR[PRED_IND][second_vertex[OR]]
        try:
            adj_ind = self._adjs[pred_ind][second_vertex[IND]].index(u_adj)
            # by symmetry, other index method below will raise ValueError too
        except ValueError as value_error:
            raise NoEdge(
                first_vertex, second_vertex, edge_index,
            ) from value_error
        if adj_ind < len(self._adjs[pred_ind][second_vertex[IND]]) - 1:
            # move the last to the place of the deleted edge and remove the last
            self._adjs[pred_ind][second_vertex[IND]][adj_ind] = (
                self._adjs[pred_ind][second_vertex[IND]].pop()
            )
        else:
            # it is the last: so just remove it
            self._adjs[pred_ind][second_vertex[IND]].pop()
        #
        # Delete v from u's successors
        #
        v_adj: IndOrIndT = (
            (
                second_vertex[IND],
                FWDOR_REVOR[first_vertex[OR]][second_vertex[OR]],
            ),
            edge_index,
        )
        succ_ind = FWDOR_REVOR[SUCC_IND][first_vertex[OR]]
        adj_ind = self._adjs[succ_ind][first_vertex[IND]].index(v_adj)
        if adj_ind < len(self._adjs[succ_ind][first_vertex[IND]]) - 1:
            # move the last to the place of the deleted edge and remove the last
            self._adjs[succ_ind][first_vertex[IND]][adj_ind] = (
                self._adjs[succ_ind][first_vertex[IND]].pop()
            )
        else:
            # it is the last: so just remove it
            self._adjs[succ_ind][first_vertex[IND]].pop()
        self._card_e -= 1

    # -*- Overloaded built-in -*-

    def __iter__(self) -> Iterator[EIndOrIndT]:
        """Iterate on oriented edges with edge index.

        Yields
        ------
        EIndOrIndT
            Oriented edges with their edge index
        """
        for v_ind in range(len(self._adjs[SUCC_IND])):
            v = (v_ind, FORWARD_INT)
            v_rev = (v_ind, REVERSE_INT)
            for w, e_ind in self._adjs[SUCC_IND][v_ind]:
                yield v, w, e_ind
                if w[OR] == FORWARD_INT:
                    yield (w[IND], ORIENT_REV[w[OR]]), v_rev, e_ind
            for u, e_ind in self._adjs[PRED_IND][v_ind]:
                if u[OR] == REVERSE_INT:
                    yield u, v, e_ind

    def __contains__(self, edge: EIndOrT) -> bool:
        """Return True if the oriented edge is in edges container.

        Parameters
        ----------
        edge: EIndOrT
            Oriented edge

        Returns
        -------
        bool
            Oriented edges in edges container
        """
        u, v = edge
        #
        # No vertices
        #
        if u[IND] >= len(self._adjs[PRED_IND]):
            return False
        if v[IND] >= len(self._adjs[PRED_IND]):
            return False
        #
        # Search in forward's successors table
        #
        if u[OR] == FORWARD_INT:
            return any(v == succ for succ, _ in self._adjs[SUCC_IND][u[IND]])
        #
        # else in reverse's predecessors table
        #
        v_rev = v[IND], ORIENT_REV[v[OR]]
        return any(
            v_rev == pred_rev
            for pred_rev, _ in self._adjs[PRED_IND][u[IND]]
        )

    def __len__(self) -> int:
        r"""Return the number of oriented edges.

        Returns
        -------
        int
            Number of oriented edges

        Notes
        -----
        :math:`\forall e \in E, \bar{e} \in E`
        """
        return 2 * self._card_e
